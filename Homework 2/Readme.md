# TCP PCAP Analysis Tool

`analysis_pcap_tcp.py` is a package written in python that allows you to quickly
analyze PCAP files generated by TCP Dumps. It just prints out some simple information
about the different flows going on.

## Dependencies

The [dpkt](https://github.com/kbandla/dpkt) package is required to run 
`analysis_pcap_tcp.py`. It can be installed through
[pip](https://pip.pypa.io/en/stable/), using the command:

```bash
pip install dpkt
```

A version of Python 3 that's compatible with dpkt must also be installed.

## Usage

How my program works is that `analyze()` inside `analysis_pcap_tcp.py` will take in a
path to a PCAP file and then loop through that PCAP file. Each packet it detects will
be compared against existing `TCPFlow` objects. If the packet belongs in an existing
flow inside the `flows[]` array, then that packet will enter that flow, otherwise a 
new flow will be created. After the program runs out of packets to analyze, then it
print out a summary of the different flows detected.

>*Note: This program will only work if new flows are created. Existing flows will be
ignored.*

To run, first `analysis_pcap_tcp.py` **and** `TCPFlow.py`
**must be in the same directory**. Then all that needs to be done is to just run:

```
python analysis_pcap_tcp.py
```

To change the PCAP file that it runs with, all thats needed is to change the path to
the PCAP in the `analyze('path')` function call on the bottom of the source file or to
run python in shell mode and call `analyze()` yourself.

## Example Output

```python
$ python analysis_pcap_tcp.py
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