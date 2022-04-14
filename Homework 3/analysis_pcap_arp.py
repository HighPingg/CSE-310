import dpkt
import struct

def analyze(file :str):
    f = open(file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    for ts, buf in pcap:
        if dpkt.ethernet.Ethernet(buf).type != dpkt.ethernet.ETH_TYPE_ARP:
            continue
        
        data = buf[14:-4]
        if len(data) == 24:
            arpPacket = dict(zip(['hwType', 'ptype',
                            'hlen', 'plen', 'opcode',
                            'sha', 'spa', 'tha', 'tpa'],
                            struct.unpack('HH', data)))
        elif len(data) == 38:
            pass

        else:
            print('Unable to parse an ARP packet.')

analyze('assignment4_my_arp.pcap')
