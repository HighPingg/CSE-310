import dpkt
import socket

f = open('PCAP files/assignment2.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

print('SYN: ', dpkt.tcp.TH_FIN)

num = 0

for ts, buf in pcap:
    try:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        # read the source IP in src
        src = socket.inet_ntoa(ip.src)
        # read the destination IP in dst
        dst = socket.inet_ntoa(ip.dst)

        tcp = ip.data

        # Print the source and destination IP
        print('Source: ', src, 'Source Port: ', tcp.sport, ' Destination: ', dst, 'Destination Port: ', tcp.dport, tcp.seq, tcp.ack, tcp.win, tcp.flags)

    except:
        pass

    num += 1
    if num == 50:
        break

f.close()