# Program Summary

## **Output for assignment2.pcap:**
```python
FLOW 1:
Sender: 130.245.145.12 (port 43498)
Receiver: 128.208.2.198 (port 80)
11106 packets (10318616 bytes - 5551983.05 Bps)

First Two Transactions:
	seq: 705669103   ack: 1921750144 | payload: 24     bytes | win: 49152 [PUSH/ACK]
	seq: 1921750144  ack: 705669127  | payload: 0      bytes | win: 49152 [ACK]

	seq: 705669127   ack: 1921750144 | payload: 1448   bytes | win: 49152 [ACK]
	seq: 1921750144  ack: 705670575  | payload: 0      bytes | win: 49152 [ACK]

Estimated RTT: 73.00 ms
First Three Congestion Windows: [12, 20, 41]

Total Packets Retransmitted: 3
Triple Duplicate ACK Count: 2
RTO Retransmitted Count: 1 


FLOW 2:
Sender: 130.245.145.12 (port 43500)
Receiver: 128.208.2.198 (port 80)
11834 packets (10453296 bytes - 1279148.61 Bps)

First Two Transactions:
	seq: 3636173852  ack: 2335809728 | payload: 24     bytes | win: 49152 [PUSH/ACK]
	seq: 2335809728  ack: 3636173876 | payload: 0      bytes | win: 49152 [ACK]

	seq: 3636173876  ack: 2335809728 | payload: 1448   bytes | win: 49152 [ACK]
	seq: 2335809728  ack: 3636175324 | payload: 0      bytes | win: 49152 [ACK]

Estimated RTT: 72.71 ms
First Three Congestion Windows: [10, 22, 33]

Total Packets Retransmitted: 94
Triple Duplicate ACK Count: 4
RTO Retransmitted Count: 90 


FLOW 3:
Sender: 130.245.145.12 (port 43502)
Receiver: 128.208.2.198 (port 80)
1185 packets (1071576 bytes - 1830677.11 Bps)

First Two Transactions:
	seq: 2558634630  ack: 3429921723 | payload: 24     bytes | win: 49152 [PUSH/ACK]
	seq: 3429921723  ack: 2558634654 | payload: 0      bytes | win: 49152 [ACK]

	seq: 2558634654  ack: 3429921723 | payload: 1448   bytes | win: 49152 [ACK]
	seq: 3429921723  ack: 2558636102 | payload: 0      bytes | win: 49152 [ACK]

Estimated RTT: 73.51 ms
First Three Congestion Windows: [20, 43, 61]

Total Packets Retransmitted: 0
Triple Duplicate ACK Count: 0
RTO Retransmitted Count: 0 
```

## Part A

**Number of Flows:**
> I've detected a total of 3 flows here. This is done simply by checking the port
numbers of the packet, checking if it matches with a current flow, otherwise 
checking if this is a new package by looking for the SYN flag.

**TCP Header:**
> seq and ack numbers as well as the payload size - `len(TCP.data)` are just pulled
directly from the TCP header. The source code for the TCP Headers as well as the
TCP class itself can be found in Github under
[dpkt.tcp.TCP](https://github.com/kbandla/dpkt/blob/master/dpkt/tcp.py).

**Window Size**
> Here, I was able to calculate the size of the TCP recv window. This was done
through finding the scaling factor (which is stored in `TCP.opts` options as code 3)
and multiplying it by `TCP.win`. To get the options, we need to parse the options
first, then iterate through these options to find the code
`dpkt.tcp.TCP_OPT_WSCALE(3)` using `dpkt.tcp.parse_opts()`. This will give us a 
window scale factor that we raise 2 to the power of that number (ie. `2**SCALE`). 
This number is then multiplied by `TCP.win` to get the calculated window size.

**Total Size of Transmitted Packets**
> This is quite simple to do. After we strip down a packet to the TCP layer, we can
find the size of it using `len(TCP)`. The dpkt.tcp.TCP
[source code](https://github.com/kbandla/dpkt/blob/master/dpkt/tcp.py) states that
it finds the length of the header, options, and the data/payload. On piazza, its
stated we should start at the first packet after the handshake has occured. I 
implemented this by piggy-backing off the code used to determine the *First Two 
Transactions* and setting the "state" of this flow to live when the first packet 
with data is detected. I stop counting the total bytes after the last packet has 
been transmitted. This is done by just checking for the `dpkt.tcp.TH_FIN` flag.
Finding the interval of time in which these packets are transmitted can be done by
just storing the timestamps in a variable when these events occur.
>> Note: It was said on the HW document that we should stop at the FIN flag, but it
was then mentioned in Piazza that we should stop at the package before FIN since
it's "not a true measure of throughput".

>Second Note: My packet counter counts ALL packets including SYNs and FINs by 
design.

**First Two Transactions**
> We first need to make a method that determines the direction a packet is going.
This is used many times throughout the program. My `TCPFlow.belongsIn()` returns 0
if the packet doesn't belong in the flow, 1 if it is outgoing (*src port match src
port on packet*) or 2 if it is incoming from the server (*src port matches dest 
port on packet*). We then just take the first and second packet that has some data
as well as doesn't have the SYN flag. For the ACK for these SYNs, it's just the
next packet thats returned from the server that has an ACK > the first packet's SEQ.

## Part B

**Finding RTT**
> The first step to finding *cwnd* is to find/estimate the RTT. I use a very simple
method which is just to find the time it takes for the initial [SYN] to get a
[SYN/ACK]. I will use this throughout the program. This isn't a great estimation, but it may suffice for the first few windows.

**Congestion Windows**
> I personally calculate the congestion windows by finding the number of packets
that are transmitted within 1 RTT of each other. Instead of instantaneously
extending the packet at the end of the last window, I extend it to 1 RTT from the
**timestamp of the next packet**. My logic behind doing this is that due to network
congestion or other factors, the sending of these packets may be delayed leading to
inaccurate results. This is kinda confirmed in the last packet. From method 1 I get
a cwnd of [20, 42, 41], meaning the window shrinked even though there was no sign of
congestion. However by extending it from the timestamp of the last packet, I get an
increase of around 20 which makes a bit more sense.

> Its also quite odd that the cwnd for the third flow is double those of the first 2.
My best guess of why this behavior exists is maybe this version of TCP detects that
the packets are going to the same server ips and thus splits the window between the
first 2 since they run concurrently while the third flow is runs alone and thus is
able to send more packets through the network.

**Detecting Packet Retransmissions**
> Retransmissions are packets that need to be sent again due to it likely being
dropped. The simplest and most time efficient way to detect retransmissions is to use
a hash map (I used a defaultdict because python). We store sequence numbers as keys
and the timestamps as the values. If a key exists already, that means this packet is
being retransmitted and we can then find the reason for this retransmission.
Otherwise, this is a new packet and we can add it to the map.

**RTO Timeout Detection**
> Detecting RTOs is quite simple now that we can detect packet retransmissions, the
timestamp of the last time that packet was transmitted, as well as the RTT. We simply
check that the time that this packet was being sent minus the time that the last
packet was sent is greater than or equal to 2 RTTs. If this criteria is met then its
very likely this packet was retransmitted.

**Triple Ack Detection**
> We already have a system to check for retransmissions so we can just piggy-back off
this. However to detect triple acks, we need to store information about acks. I
implemented a queue of size 3 that stores the 3 most recent acks. When there is a
retransmission, we can just check if the past 3 acks are the same and the number is
less than or equal to the sequence number of the retransmitted package. If both these
conditions are met, then this package was likely retransmitted due to triple duplicate
ack. Any package that wasn't retransmitted due to RTO timeout or Triple Ack was
retransmitted for some other reason not defined in the homework instructions.