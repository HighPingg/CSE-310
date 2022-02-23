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

# TESTING MY DIG
# # from mydig import mydig

# # for url in TEST_URLS:
# #     mydig(url)
# OUTPUT FROM HERE WAS REDIRECTED

# # with open('./test_results/mydigresults.txt') as f:
# #     output = f.read().splitlines()
# #     output = list(filter(lambda x: 'Query time: ' in x, output))

# # for i in range(len(output)):
# #     print(output[i].split(' ')[2], '-', TEST_URLS[i])


# TESTING LOCAL AND PUBLIC DNS RESOLVER
import dns.resolver
from time import time

my_resolver = dns.resolver.Resolver()

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = ['8.8.8.8']

for domain in TEST_URLS:
    timeElapsed = time()
    answer = my_resolver.resolve(domain)
    timeElapsed = round((time() - timeElapsed) * 1000)
    
    print(timeElapsed, '-', domain)