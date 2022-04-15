# Sample Pinger

## Explainations
```
1. Firstly, the localhost has a send time of 0 ms. Makes sense because when contacting
the localhost, it will just go to the loopback device to simulate an incoming network
packet even though the packet never really leaves the device.

2. When contacting to cs.stonybrook.edu, the ping round trip time takes around 15
ms on average. This is very fast and it makes sense since although I'm in the city,
the stonybrook server is only a few routers away.

3. When contacting root servers, we see some more interesting results. We see the
fastest of these servers is the Los Angeles root server taking around 24 ms on 
average. This is probably due to there being a direct connection between New York City
and Los Angeles due to the sheer amount of traffic that flows between the two cities.
It is also geographically closer that the other few root servers.

I contacted two root servers in the EU in Stockholm and in Amsterdam. The Stockholm
server was seeing around an average RTT of 96 ms while the Amsterdam server is seeing 
around 47 ms RTT. It makes sense that these connections take longer to ping than the
ones in the USA, but what doesn't make much sense is the server in Stockholm taking
almost the same of that of Japan. The root server in Tokyo took around 82 ms which is
quite fast considering the distance the packet has to travel compared to the
Stockholm time. This might be due to either the Swedish server serving a large amount
or maybe there being less hops necessary to reach the Japanese root server.
```

## Localhost Test (127.0.0.1)
```python
$ python sample_pinger.py localhost
Pinging 127.0.0.1 using Python:
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
36 bytes received from 127.0.0.1; time=0.0
--- localhost ping statistics ---
Round Trip Min: 0.00 ms
Round Trip Max: 0.00 ms
Round Trip Avg: 0.00 ms
```

## cs.stonybrook.edu (23.185.0.2)
```python
$ python sample_pinger.py cs.stonybrook.edu
Pinging 23.185.0.2 using Python:
36 bytes received from 23.185.0.2; time=0.0205385684967041
36 bytes received from 23.185.0.2; time=0.016228437423706055
36 bytes received from 23.185.0.2; time=0.0062944889068603516
36 bytes received from 23.185.0.2; time=0.019793272018432617
36 bytes received from 23.185.0.2; time=0.01800847053527832
36 bytes received from 23.185.0.2; time=0.01394343376159668
36 bytes received from 23.185.0.2; time=0.012800455093383789
36 bytes received from 23.185.0.2; time=0.01421213150024414
36 bytes received from 23.185.0.2; time=0.014791011810302734
36 bytes received from 23.185.0.2; time=0.01724386215209961
36 bytes received from 23.185.0.2; time=0.01679539680480957
36 bytes received from 23.185.0.2; time=0.013993978500366211
36 bytes received from 23.185.0.2; time=0.014785528182983398
36 bytes received from 23.185.0.2; time=0.01880335807800293
36 bytes received from 23.185.0.2; time=0.014911174774169922
36 bytes received from 23.185.0.2; time=0.016809701919555664
--- cs.stonybrook.edu ping statistics ---
Round Trip Min: 6.29 ms
Round Trip Max: 20.54 ms
Round Trip Avg: 15.62 ms
```

## Tokyo Root Server (202.12.27.33)
```python
$ python sample_pinger.py 202.12.27.33
Pinging 202.12.27.33 using Python:
36 bytes received from 202.12.27.33; time=0.08939051628112793
36 bytes received from 202.12.27.33; time=0.08784627914428711
36 bytes received from 202.12.27.33; time=0.08264350891113281
36 bytes received from 202.12.27.33; time=0.08220839500427246
36 bytes received from 202.12.27.33; time=0.08266925811767578
36 bytes received from 202.12.27.33; time=0.08029389381408691
36 bytes received from 202.12.27.33; time=0.07978200912475586
36 bytes received from 202.12.27.33; time=0.07899260520935059
36 bytes received from 202.12.27.33; time=0.08082461357116699
--- 202.12.27.33 ping statistics ---
Round Trip Min: 78.99 ms
Round Trip Max: 89.39 ms
Round Trip Avg: 82.74 ms
```

## Amseterdam Root Server (193.0.14.129)
```python
Pinging 193.0.14.129 using Python:
36 bytes received from 193.0.14.129; time=0.04436087608337402
36 bytes received from 193.0.14.129; time=0.04381275177001953
36 bytes received from 193.0.14.129; time=0.0689697265625
36 bytes received from 193.0.14.129; time=0.04844522476196289
36 bytes received from 193.0.14.129; time=0.0379176139831543
36 bytes received from 193.0.14.129; time=0.047811031341552734
36 bytes received from 193.0.14.129; time=0.04448699951171875
36 bytes received from 193.0.14.129; time=0.0388185977935791
36 bytes received from 193.0.14.129; time=0.05053877830505371
36 bytes received from 193.0.14.129; time=0.04582643508911133
--- 193.0.14.129 ping statistics ---
Round Trip Min: 37.92 ms
Round Trip Max: 68.97 ms
Round Trip Avg: 47.10 ms
```

## Stockholm Root Server (192.36.148.17)
```python
$ python sample_pinger.py 192.36.148.17
Pinging 192.36.148.17 using Python:
36 bytes received from 192.36.148.17; time=0.0949864387512207
36 bytes received from 192.36.148.17; time=0.09598755836486816
36 bytes received from 192.36.148.17; time=0.09840226173400879
36 bytes received from 192.36.148.17; time=0.09582972526550293
36 bytes received from 192.36.148.17; time=0.09376406669616699
36 bytes received from 192.36.148.17; time=0.08899259567260742
36 bytes received from 192.36.148.17; time=0.10100221633911133
36 bytes received from 192.36.148.17; time=0.10551857948303223
36 bytes received from 192.36.148.17; time=0.09679841995239258
--- 192.36.148.17 ping statistics ---
Round Trip Min: 88.99 ms
Round Trip Max: 105.52 ms
Round Trip Avg: 96.81 ms
```

## Los Angeles Root Server (199.7.83.42)
```python
$ python sample_pinger.py 199.7.83.42
Pinging 199.7.83.42 using Python:
36 bytes received from 199.7.83.42; time=0.03602933883666992
36 bytes received from 199.7.83.42; time=0.0200042724609375
36 bytes received from 199.7.83.42; time=0.04681968688964844
36 bytes received from 199.7.83.42; time=0.016791343688964844
36 bytes received from 199.7.83.42; time=0.014003276824951172
36 bytes received from 199.7.83.42; time=0.027759790420532227
36 bytes received from 199.7.83.42; time=0.020547866821289062
36 bytes received from 199.7.83.42; time=0.020555973052978516
36 bytes received from 199.7.83.42; time=0.017795324325561523
36 bytes received from 199.7.83.42; time=0.03259778022766113
36 bytes received from 199.7.83.42; time=0.02173328399658203
36 bytes received from 199.7.83.42; time=0.020790815353393555
36 bytes received from 199.7.83.42; time=0.021029949188232422
--- 199.7.83.42 ping statistics ---
Round Trip Min: 14.00 ms
Round Trip Max: 46.82 ms
Round Trip Avg: 24.34 ms
```
> Wasn't able to find a fourth root server outside the USA.

