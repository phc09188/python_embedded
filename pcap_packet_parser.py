import csv
from datetime import datetime
from scapy.all import rdpcap, raw
from scapy.layers.inet import IP, TCP, UDP


# .pcap 파일의 모든 data 값을 csv로 저장
def raw_to_hex(data):
    return data.hex()
def extract_string(data, start_marker, length):
    try:
        # 문자열로 변환
        data_str = data.decode(errors='ignore')
        start_index = data_str.find(start_marker)
        if start_index != -1:
            return start_index,data_str[start_index:start_index + length]
    except Exception as e:
        print(f"Error: {e}")
    return 0,None


# Specify the .pcap file to read
file_path = "D:/사이클 작업(j0104041-j0211032).pcapng"

# Read the packets from the pcap file
packets = rdpcap(file_path)

# Open the result CSV file for writing
with open('../packet_result.csv', mode='w', newline='') as csv_file:
    # Define the CSV writer
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(["Packet Time", "Source IP", "Destination IP", "Protocol", "Length", "CODE", "Data"])

    # Iterate through each packet
    for packet in packets:
        # Check if the packet has an IP layer
        if (packet.haslayer('IP') and
            (packet['IP'].src == '192.168.10.111' or packet['IP'].dst == '192.168.10.111')):
            # Extract packet time, source IP, destination IP, protocol, length, and data
            packet_time = datetime.fromtimestamp(packet.time).strftime('%H:%M:%S.%f')
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            length = len(packet)
            raw_data = bytes(raw(packet))
            start_index, extracted_string = extract_string(raw_data,"5C",length)
            data = raw_to_hex(raw_data)
            data = data[start_index:]
            if proto == 6:
                protocol = "TCP"
            elif proto == 17:
                protocol = "UDP"
            else:
                protocol = "Other"
            if extracted_string:
                writer.writerow([packet_time, src_ip, dst_ip, protocol, length, extracted_string[0:8], data])
            else:
                writer.writerow([packet_time, src_ip, dst_ip, protocol, length, '',''])
