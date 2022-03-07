import dpkt
from TCPFlow import TCPFlow

f = open('PCAP files/assignment2.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

num = 0
flows = []

for ts, buf in pcap:
    # if num < 50:
    #     num += 1
    #     print(ts)
    
    ip = dpkt.ethernet.Ethernet(buf).data

    # Check to make sure it's a TCP connection.
    if ip.p != dpkt.ip.IP_PROTO_TCP:
        continue

    # Check if ip already in flows
    newFlow = True
    for flow in flows:
        if flow.belongsIn(ip):
            flow.addPacket(ts, ip)
            newFlow = False
            break

    if newFlow:
        flows.append(TCPFlow(ts, ip))

for flow in flows:
    print(flow, '\n\n')
    
    # for ip in flow.pastPacks:
    #     print('\t', TCPFlow.getTCPInfo(ip.data))


f.close()
