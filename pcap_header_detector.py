import csv
from datetime import datetime
from scapy.all import rdpcap, raw
from scapy.layers.inet import IP, TCP, UDP

# .pcap파일에서 header 찾는 작업

file_path = "D:/사이클 작업(j0104041-j0211032).pcapng"

ip = "192.168.10.111"
port = [7000, 7111]
packets = rdpcap(file_path)

with open("result.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["시간", "SRC_IP", "SRC_PORT", "DST_IP", "DST_PORT", "TCP_LEN", "HDR_LEN", "HEADER", "PACKET"])

    for packet in packets:
        #if IP in packet and packet[IP].src == '192.168.10.111' and TCP in packet:
        if TCP in packet:
            if (packet[IP].src == ip or packet[IP].dst == ip): #and (packet.sport == port or packet.dport == port):
                #if not packet.haslayer(Padding):
                if not packet[TCP].flags & 2:       #SYN 일때, load가 없음.
                    if packet[TCP].payload.load[0] != 0:
                        if len(packet[TCP].payload.load) > 8:
                            #print(type(packet.time), packet[TCP].payload.load)
                            #print(datetime.fromtimestamp(float(packet.time)), packet[TCP].payload.load[:8].decode(), packet[TCP].payload.load)
                            writer.writerow([datetime.fromtimestamp(float(packet.time)).strftime('%H-%M-%S.%f'),
                                             packet[IP].src, packet.sport, packet[IP].dst, packet.dport,
                                             len(packet[TCP].payload.load), packet[TCP].payload.load[23:26].decode(),
                                             packet[TCP].payload.load[3:8].decode(), packet[TCP].payload.load])
                        else:
                            writer.writerow([datetime.fromtimestamp(float(packet.time)).strftime('%H-%M-%S.%f'),
                                             packet[IP].src, packet.sport, packet[IP].dst, packet.dport,
                                             len(packet[TCP].payload.load), "0",
                                             packet[TCP].payload.load])