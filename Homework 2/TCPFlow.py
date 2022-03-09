from collections import defaultdict

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
        self.throughput = 0
        self.numPackets = 1
        self.receiverWindowScale = None

        self.senderWindowScale = None
        for code, val in dpkt.tcp.parse_opts(ip.data.opts):
            if code == dpkt.tcp.TCP_OPT_WSCALE:
                self.senderWindowScale = val

        self.startTime = timestamp
        self.endTime = None
        self.firstPacketTime = None
        self.previousPacketTime = timestamp
        
        self.RTT = None
        self.endOfWindow = 0
        self.congestionWindows = []
        self.windowCount = 0

        # Store past packet data directly
        self.firstTwo = ([], [])
        self.ackWindow = []
        self.pastPacks = defaultdict(int)
        self.totalRetransmitted = 0
        self.tripleAckRetransmitted = 0
        self.timeoutRetransmitted = 0

        # Flow state will keep track of the state of this flow.
        # 0 - Initializing
        # 1 - Live Flow
        # 2 - FIN sent
        self.status = 0

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
    def addPacket(self, timestamp:int, ip:dpkt.ip.IP):

        self.numPackets += 1

        # If this is the second packet, then this is probably the SYN/ACK. We can use this to estimate
        # the RTT.
        if self.numPackets == 2:
            self.RTT = timestamp - self.startTime

            for code, val in dpkt.tcp.parse_opts(ip.data.opts):
                if code == dpkt.tcp.TCP_OPT_WSCALE:
                    self.receiverWindowScale = val

        # If the first 2 packets haven't been added yet, we check if the current packet isn't a SYN,
        # it has a payload, and the senders and receivers match. If this criteria is met, we can add
        # it to the firstTwo list.
        tcp = ip.data
        if len(self.firstTwo[0]) < 2 or len(self.firstTwo[1]) < 2:
            if (not tcp.flags & TCPFlow.TCP_FLAGS['SYN']):
                direction = self.belongsIn(ip)
                
                # If it's outgoning, check if it has a payload and finds an empty array to place it in
                if direction == 1 and len(tcp.data) != 0:
                    if len(self.firstTwo[0]) == 0:
                        self.firstTwo[0].append(tcp)

                        # Here we see the first packet with a payload being sent so the connection is
                        # now live
                        self.status = 1
                        self.firstPacketTime = timestamp
                        self.endOfWindow = timestamp

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
        
        # Detects if FIN is sent from the user
        if self.belongsIn(ip) == 1 and tcp.flags & TCPFlow.TCP_FLAGS['FIN']:
            self.status = 2
            self.endTime = self.previousPacketTime


        # As the connection is live, we add packets to the throughput
        if self.status == 1 and self.belongsIn(ip) == 1:
            self.throughput += len(tcp)
            # self.pastPacks += [ip]


        # Here we can start queueing incoming acks and determine whether or not we see duplicate ones
        if self.belongsIn(ip) == 2:
            self.ackWindow.append(tcp.ack)

            # If there are 3 acks currently, then we can dequeue the first one then add the next ack number.
            if len(self.ackWindow) > 3:
                self.ackWindow.pop(0)


        # Here we keep track of retransmitted packages using a hashmap. We keep track of the timestamp and
        # then find the reason as to why they were retransmitted.
        if self.belongsIn(ip) == 1:
            # If this is a new packet, then we can take note of the timestamp and continue.
            if self.pastPacks[tcp.seq] == 0:
                self.pastPacks[tcp.seq] = timestamp
            else:
                # Slight edge case when the first packet is piggy backed off the ACK, then it uses the same
                # sequence number, thus causing a possible false positive retranmit detection. We can just
                # check that the timestamp of this packet isn't the first packet.
                if timestamp != self.firstPacketTime:
                    self.totalRetransmitted += 1
                # Check to see if the retransmit timeout happened. This means 2 RTTs have passed since the
                # last time this packet was sent.
                if (timestamp - self.pastPacks[tcp.seq]) >= (2 * self.RTT):
                    self.timeoutRetransmitted += 1

                # Check to see if we have a triple ack
                if len(self.ackWindow) == 3 and all(x == self.ackWindow[0] for x in self.ackWindow):
                    self.tripleAckRetransmitted += 1


        # Once we are in the live stage, we can now estimate the size of the congestion windows. We do
        # this by finding how many RTTs this packet falls in while the connection is live and then putting
        # it into the correct space in the congestionWindows list.
        if self.windowCount <= 3 and self.status == 1 and self.belongsIn(ip) == 1:
            # If the current timestamp is greater than the end of window, we need to extend it and move to
            # the next window.
            if self.endOfWindow <= timestamp:
                self.congestionWindows.append(0)
                self.endOfWindow = timestamp + self.RTT
                self.windowCount += 1
            
            if len(self.congestionWindows) > 3:
                self.congestionWindows = self.congestionWindows[:-1]
            else:
                self.congestionWindows[-1] += 1

        # if len(self.pastPacks) < 30:
        #     self.pastPacks.append(ip)
        if self.belongsIn(ip) == 1:
            self.previousPacketTime = timestamp

    # Returns general info about this flow
    def __str__(self):
        senderIP = 'Sender: {} (port {})'.format(socket.inet_ntoa(self.sender), self.initialSYN.sport)
        receiverIP = 'Receiver: {} (port {})'.format(socket.inet_ntoa(self.receiver), self.initialSYN.dport)

        speed = self.throughput / (self.endTime - self.firstPacketTime)
        packs = '{} packets ({} bytes - {:.2f} Bps)'.format(self.numPackets, self.throughput, speed)

        estimatedRTT = 'Estimated RTT: {:.2f} ms'.format(self.RTT * 1000)

        tripleAck = 'Triple Duplicate ACK Count: {}'.format(self.tripleAckRetransmitted)

        firstTwoTrans = 'First Two Transactions:\n'
        for ip in self.firstTwo:
            for tcp in ip:
                firstTwoTrans += '\t{}\n'.format(self.getTCPInfo(tcp))
            firstTwoTrans += '\n'

        firstCongestionWindows = 'First Three Congestion Windows: {}'.format(self.congestionWindows)

        totalRetrans = 'Total Packets Retransmitted: {}'.format(self.totalRetransmitted)
        timeout = 'RTO Retransmitted Count: {}'.format(self.timeoutRetransmitted)

        return '{}\n{}\n{}\n\n{}{}\n{}\n\n{}\n{}\n{}'.format(senderIP, receiverIP, packs,
                            firstTwoTrans, estimatedRTT, firstCongestionWindows, totalRetrans, tripleAck, timeout)
    
    # Prints out important info given a TCP object
    def getTCPInfo(self, tcp: dpkt.tcp.TCP):
        # Adds flag strings
        flags = ''
        for flagString in TCPFlow.TCP_FLAGS:
            if tcp.flags & TCPFlow.TCP_FLAGS[flagString]:
                flags += flagString + '/'
    
        # Find window size by checking which direction this tcp request is going. We assume that the package
        # belongs in this flow (ie. port and ip addresses are the same)
        window = tcp.win
        if self.initialSYN.sport == tcp.sport:
            window *= 2 ** int.from_bytes(self.senderWindowScale, 'big')
        else:
            window *= 2 ** int.from_bytes(self.receiverWindowScale, 'big')

        if len(flags) != 0:
            # Strip the last '/' from flag string
            flags = flags[:-1]

        return 'seq: {:<10}  ack: {:<10} | payload: {:<6} bytes | win: {:<4} [{}]'.format(
                                                            tcp.seq, tcp.ack, len(tcp.data), window, flags)

