import dpkt
from TCPFlow import TCPFlow

f = open('PCAP files/cs.stonybrook.edu.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

num = 0
flows = []

for ts, buf in pcap:
    ip = dpkt.ethernet.Ethernet(buf).data
    
    # Check to make sure it's a TCP connection.
    if ip.p != dpkt.ip.IP_PROTO_TCP:
        continue

    # Check if ip already in flows
    newFlow = True
    for flow in flows:
        if flow.belongsIn(ip):
            flow += ip
            newFlow = False
            break

    if newFlow:
        flows.append(TCPFlow(ts, ip))

for flow in flows:
    print(flow, '\n')
    
    print('First Two Transactions:')
    for ip in flow.firstTwo:
        for tcp in ip:
            print('\t', TCPFlow.getTCPInfo(tcp))
        print()

    print()

f.close()
