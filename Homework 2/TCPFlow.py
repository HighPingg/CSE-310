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

        # Saves the whole TCP packet for port nums and starting sequence numbers
        self.initialSYN = ip.data

        # Initialize to the first packet sent
        self.throughput = len(ip.data)
        self.numPackets = 1
        self.beginTime = timestamp

        # Store past packet data directly
        self.pastPacks = [ip]
        self.firstTwo = ([], [])

    # Detects whether a packet is part of this TCP Flow
    # 0 - Not in this flow
    # 1 - Outgoing packet
    # 2 - Incoming packet
    def belongsIn(self, ip:dpkt.ip.IP):
        dstTCP = ip.data

        # Just detects if the 2 nodes have the same ip and destination ports
        if self.sender == ip.src and self.receiver == ip.dst:
            if self.initialSYN.sport == dstTCP.sport and self.initialSYN.dport == dstTCP.dport:
                return 1

        # Otherwise checks the reverse if this is from the receiver to the sender
        elif self.sender == ip.dst and self.receiver == ip.src:
            if self.initialSYN.sport == dstTCP.dport and self.initialSYN.dport == dstTCP.sport:
                return 2
        
        # If all these checks fail, then it musn't be part of this flow
        return 0

    # Overrides the add operator to add packet info to this flow
    def __add__(self, ip:dpkt.ip.IP):
        self.throughput += len(ip.data)
        self.numPackets += 1

        # If the first 2 packets haven't been added yet, we check if the current packet isn't a SYN,
        # it has a payload, and the senders and receivers match. If this criteria is met, we can add
        # it to the firstTwo list.
        tcp = ip.data
        if len(self.firstTwo[0]) < 2 or len(self.firstTwo[1]) < 2:
            if (not tcp.flags & TCPFlow.TCP_FLAGS['SYN']):
                direction = self.belongsIn(ip)
                
                # If it's outgoming, check if it has a payload and finds an empty array to place it in
                if direction == 1 and len(tcp.data) != 0:
                    if len(self.firstTwo[0]) == 0:
                        self.firstTwo[0].append(tcp)
                    elif len(self.firstTwo[1]) == 0:
                        self.firstTwo[1].append(tcp)
                
                # If it's incoming, then we check to see if the first packet is there and the ack is
                # greater than that of the first packet's sequence number.
                elif direction == 2:
                    if len(self.firstTwo[0]) == 1:
                        if tcp.ack > self.firstTwo[0][0].seq:
                            self.firstTwo[0].append(tcp)
                    elif len(self.firstTwo[1]) == 1:
                        if tcp.ack > self.firstTwo[1][0].seq:
                            self.firstTwo[1].append(tcp)
        

        if len(self.pastPacks) < 30:
            self.pastPacks.append(ip)

        return self
    
    # Returns general info about this flow
    def __str__(self):
        senderIP = 'Sender: {} (port {})'.format(socket.inet_ntoa(self.sender), self.initialSYN.sport)
        receiverIP = 'Receiver: {} (port {})'.format(socket.inet_ntoa(self.receiver), self.initialSYN.dport)
        packs = '{} packets ({} bytes)'.format(self.numPackets, self.throughput)
        
        return '{}\n{}\n{}'.format(senderIP, receiverIP, packs)
    
    # Prints out important info given a TCP object
    def getTCPInfo(tcp: dpkt.tcp.TCP):
        # Adds flag strings
        flags = ''
        for flagString in TCPFlow.TCP_FLAGS:
            if tcp.flags & TCPFlow.TCP_FLAGS[flagString]:
                flags += flagString + '/'
    
        if len(flags) != 0:
            # Strip the last '/' from flag string
            flags = flags[:-1]

        return 'seq: {:<10}  ack: {:<10} | payload: {:<6} bytes | win: {:<4} [{}]'.format(
                                                            tcp.seq, tcp.ack, len(tcp.data), tcp.win, flags)

