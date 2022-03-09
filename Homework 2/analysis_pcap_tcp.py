import dpkt
from TCPFlow import TCPFlow

def analyze(file: str):
    f = open(file, 'rb')
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

        if newFlow and (ip.data.flags & dpkt.tcp.TH_SYN):
            flows.append(TCPFlow(ts, ip))

    for flow in flows:
        print('FLOW', str(flows.index(flow) + 1) + ':')
        print(flow, '\n\n')
        
        # for ip in flow.pastPacks:
        #     print('\t', TCPFlow.getTCPInfo(ip.data))


    f.close()

analyze('PCAP files/assignment2.pcap')