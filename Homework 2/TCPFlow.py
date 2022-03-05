import dpkt
import socket

class TCPFlow:
    TCP_FLAGS = dict({
            'FIN': dpkt.tcp.TH_FIN,
            'SYN': dpkt.tcp.TH_SYN,
            'RST': dpkt.tcp.TH_RST,
            'PUSH': dpkt.tcp.TH_PUSH,
            'ACK': dpkt.tcp.TH_ACK,
            'URG': dpkt.tcp.TH_URG,
            'ECE': dpkt.tcp.TH_ECE,
            'CWR': dpkt.tcp.TH_CWR,
            'NS': dpkt.tcp.TH_NS,
        })

    def __init__(self, timestamp:int ,ip:dpkt.ip.IP):
        self.sender = ip.src
        self.receiver = ip.dst

        self.initialSYN = ip.data

        self.throughput = len(ip.data)
        self.numPackets = 1
        self.beginTime = timestamp

        self.pastPacks = [ip]

    def belongsIn(self, ip:dpkt.ip.IP):
        dstTCP = ip.data

        # Just detects if the 2 nodes have the same ip and destination ports
        if self.sender == ip.src and self.receiver == ip.dst:
            if self.initialSYN.sport == dstTCP.sport and self.initialSYN.dport == dstTCP.dport:
                return True

        elif self.sender == ip.dst and self.receiver == ip.src:
            if self.initialSYN.sport == dstTCP.dport and self.initialSYN.dport == dstTCP.sport:
                return True

        return False

    def __add__(self, ip:dpkt.ip.IP):
        self.throughput += len(ip.data)
        self.numPackets += 1

        if len(self.pastPacks) < 30:
            self.pastPacks.append(ip)

        return self

    def __str__(self):
        senderIP = 'Sender: {} (port {})'.format(socket.inet_ntoa(self.sender), self.initialSYN.sport)
        receiverIP = 'Receiver: {} (port {})'.format(socket.inet_ntoa(self.receiver), self.initialSYN.dport)
        packs = '{} packets ({} bytes)'.format(self.numPackets, self.throughput)
        
        return '{}\n{}\n{}'.format(senderIP, receiverIP, packs)

    def getFlags(ip: dpkt.ip.IP):
        return ip.data.flags

    def getTCPInfo(tcp: dpkt.tcp.TCP):
        flags = ''
        for flagString in TCPFlow.TCP_FLAGS:
            if tcp.flags & TCPFlow.TCP_FLAGS[flagString]:
                flags += flagString + '/'
    
        if len(flags) != 0:
            # Strip the last '/' from flag string
            flags = flags[:-1]

        return 'seq: {:<10}\tack: {:<10} - payload: {:<6} bytes\t[{}]'.format(tcp.seq, tcp.ack, len(tcp.data), flags)
