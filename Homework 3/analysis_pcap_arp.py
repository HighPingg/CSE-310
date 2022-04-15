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

def printARPacket(arpPacket):
    print(OPCODE_TYPE[arpPacket['opcode']])
    print('Hardware Type:', arpPacket['hwType'], '({})'.format(HARDWARE_TYPE[arpPacket['hwType']]))
    print('Protocol Type:', arpPacket['ptype'])
    print('Hardware Size:', arpPacket['hlen'])
    print('Protocol Size:', arpPacket['plen'])
    print('Opcode:', arpPacket['opcode'])
    print('Sender MAC Address:', bytesToIP(arpPacket['sha']))
    print('Sender IP Address:', bytesToIP(arpPacket['spa']))
    print('Target MAC Address:', bytesToIP(arpPacket['tha']))
    print('Target IP Address:', bytesToIP(arpPacket['tpa']))

def analyze(file :str):
    f = open(file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    arr = []

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

        # If this is a request and this is a new packet, then we can add a new entry in the
        # array.
        if arpPacket['opcode'] == 1:
            newPacket = True
            for entry in arr:
                if entry[0] == arpPacket:
                    newPacket = False
                    break
            
            if newPacket:
                arr.append([arpPacket])
        
        elif arpPacket['opcode'] == 2:
            for i in range(len(arr)):
                if arr[i][0]['tpa'] == arpPacket['spa'] and arr[i][0]['sha'] == arpPacket['tha']:
                    arr[i].append(arpPacket)
                    break
    
    for entry in arr:
        if len(entry) >= 2:
            printARPacket(entry[0])
            print()

            printARPacket(entry[1])
            print()

analyze('assignment4_my_arp.pcap')
