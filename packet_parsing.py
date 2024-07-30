import os
'''
tx rx로 이루어진 패킷을 파싱하는 code
'''

def parse_response(fw, f_code, start_addr, line):
    one = line.split(' : ')
    if one[0].startswith("[RTU]>Rx >"):
        str_packet = one[1].strip().split()
        frame = [int(hex_val, 16) for hex_val in str_packet]
        cnt = frame[2]
        if f_code == 'C' or f_code == 'D':
            for i in range(cnt):
                fw.write(format(frame[3 + i], "02X"))
                fw.write(' ')
        else:
            fw.write("\n")
            for i in range(0, cnt, 2):
                reg_val = frame[3 + i] << 8 | frame[4 + i]
                # pair_val = f"{int(start_addr + i/2)}: {format(reg_val, '04X')}\n"
                pair_val = f"{int(start_addr + i / 2)}: {reg_val}\n"
                fw.write(pair_val)
        fw.write("\n")
    else:
        print(line)
        raise Exception("Failed 3")


def start_parse(file_name):
    f = open(file_name, "r", encoding='utf8')
    if not f:
        print("read file open failed")
    dir_file = os.path.split(file_name)
    wfile = "_" + dir_file[1]
    wfile = os.path.join(dir_file[0], wfile)
    fw = open(wfile, "w", encoding='utf8', newline='\n')
    if not fw:
        print("write file open failed")

    while True:
        line = f.readline().strip()
        if not line:
            break

        one = line.split(' : ')
        if one[0].startswith("[RTU]>Tx >"):
            str_packet = one[1].strip().split()
            frame = [int(hex_val, 16) for hex_val in str_packet]
            start_addr = frame[2] << 8 | frame[3]
            count = frame[4] << 8 | frame[5]
            if frame[1] == 1:
                f_code = "C"
            elif frame[1] == 2:
                f_code = "D"
            elif frame[1] == 3:
                f_code = "H"
            elif frame[1] == 4:
                f_code = "I"
            else:
                print(line)
                raise Exception("Failed 1")
            fw.write(f"{f_code}: {start_addr}: {count}: ")
            parse_response(fw, f_code, start_addr, f.readline().strip())
        else:
            print(line)
            raise Exception("Failed 2")
    f.close()
    fw.close()


if __name__ == "__main__":
    start_parse(r"D:\KP1000_1")
    start_parse(r"D:\DP1000_2.txt")
    start_parse(r"D:\DP1000_3.txt")
    start_parse(r"D:\DP1000_4.txt")

    '''
    원본 파일 위치를 위에서 수정 / -> / 로 변경
    cmd -> d:
    cd temp
    python a.py

    '''
