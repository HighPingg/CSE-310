# ARP Packet Analysis
## Run Demo
```python
$ python analysis_pcap_arp.py
ARP Request
Hardware Type: 1 (Ethernet)
Protocol Type: 2048
Hardware Size: 6
Protocol Size: 4
Opcode: 1
Sender MAC Address: 14:59:c0:ac:79:c9
Sender IP Address: 192:168:1:1
Target MAC Address: 00:00:00:00:00:00
Target IP Address: 192:168:1:9

ARP Reply
Hardware Type: 1 (Ethernet)
Protocol Type: 2048
Hardware Size: 6
Protocol Size: 4
Opcode: 2
Sender MAC Address: c0:b6:f9:aa:9b:64
Sender IP Address: 192:168:1:9
Target MAC Address: 14:59:c0:ac:79:c9
Target IP Address: 192:168:1:1
```

The IP of my router is 192.168.1.1 and the MAC address is 14:59:c0:ac:79:c9 based on
the request and reply. We see that the sender requesting to map an IP is comes from
that IP and MAC address as well as the reply has that exact target set.