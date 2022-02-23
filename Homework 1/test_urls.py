TEST_URLS = [ 'Wikipedia.org'
            , 'Zoom.us'
            , 'Live.com'
            , 'Netflix.com'
            , '360.cn'
            , 'Chaturbate.com'
            , 'Yahoo.co.jp'
            , 'Bongacams.com'
            , 'Amazon.in'
            , 'Google.com.hk'
            ]

# # TESTING MY DIG
# from mydig import mydig

# for url in TEST_URLS:
#     for _ in range(10):
#         mydig(url)
# OUTPUT FROM HERE WAS REDIRECTED

# with open('./test_results/mydigresults.txt') as f:
#     output = f.read().splitlines()
#     output = list(filter(lambda x: 'Query time: ' in x, output))

# times = []
# for i in range(len(output)):
#     times.append(int(output[i].split(' ')[2]))

#     if i % 10 == 9:
#         print(times, TEST_URLS[int(i / 10)])
#         times = []


# # TESTING LOCAL AND PUBLIC DNS RESOLVER
# import dns.resolver
# from time import time

# my_resolver = dns.resolver.Resolver()

# # 8.8.8.8 is Google's public DNS server
# #my_resolver.nameservers = ['8.8.8.8']

# for domain in TEST_URLS:
#     times = []
#     for _ in range(10):
#         timeElapsed = time()
#         answer = my_resolver.resolve(domain)
#         timeElapsed = round((time() - timeElapsed) * 1000)

#         times.append(timeElapsed)
    
#     print(times, domain)