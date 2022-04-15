import dpkt
import struct

OPCODE_TYPE = {
    1 : 'ARP Request',
    2 : 'ARP Reply',
    3 : 'RARP Request',
    4 : 'RARP Reply',
    5 : 'DRARP Request',
    6 : 'DRARP Reply',
    7 : 'DRARP Error',
    8 : 'InARP Request',
    9 : 'InARP Reply',
}

HARDWARE_TYPE = {
    1 : 'Ethernet',
    6 : 'IEE 802 Network',
    7 : 'ARCNET',
    15 : 'Frame Relay',
    16 : 'Asynchronous Transfer Mode',
    17 : 'HDLC',
    18 : 'Fibre Channel',
    19 : 'Asynchronous Transfer Mode',
    20 : 'Serial Line'
}

def bytesToIP(bytesArr):
    formatString = ''
    for _ in range(len(bytesArr)):
        formatString += 'B'

    resultString = ''
    for byte in struct.unpack(formatString, bytesArr):
        if len(bytesArr) == 6:
            resultString += '{:02x}'.format(byte)
        else:
            resultString += str(byte)
        
        resultString += ':'

    return resultString[:-1]

def analyze(file :str):
    f = open(file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    for ts, buf in pcap:
        # ARP packets will be at least size 42. Anything else is not an ARP packet.
        if len(buf) < 42:
            continue

        # ARP packet starts after the link layer protocol (Ethernet II) and is 28 bytes
        # in size.
        data = buf[14:42]
        arpPacket = dict(zip(['hwType', 'ptype',
                        'hlen', 'plen', 'opcode',
                        'sha', 'spa', 'tha', 'tpa'],
                        struct.unpack('!HHBBH6s4s6s4s', data)))
        
        # ARP packet has a protocol type of 2048. Anything else is not an ARP packet.
        if arpPacket['ptype'] != 2048:
            continue

        print('ARP Packet:')
        print('Hardware Type:', arpPacket['hwType'], '({})'.format(HARDWARE_TYPE[arpPacket['hwType']]))
        print('Protocol Type:', arpPacket['ptype'])
        print('Hardware Size:', arpPacket['hlen'])
        print('Protocol Size:', arpPacket['plen'])
        print('Opcode:', arpPacket['opcode'], '({})'.format(OPCODE_TYPE[arpPacket['opcode']]))
        print('Sender MAC Address:', bytesToIP(arpPacket['sha']))
        print('Sender IP Address:', bytesToIP(arpPacket['spa']))
        print('Target MAC Address:', bytesToIP(arpPacket['tha']))
        print('Target IP Address:', bytesToIP(arpPacket['tpa']))
        print()

analyze('assignment4_my_arp.pcap')
