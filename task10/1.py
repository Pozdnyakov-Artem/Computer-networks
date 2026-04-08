import re
import subprocess

import pandas as pd


def dig(host):
    ipv4 = subprocess.run(['dig', host, '+short'],capture_output=True,text=True,encoding='cp866')
    ipv6 = subprocess.run(['dig', 'AAAA', host, '+short'], capture_output=True, text=True, encoding='cp866')
    return ipv4.stdout, ipv4.returncode, ipv6.stdout, ipv6.returncode

def traceroute(ip_v4):
    route = subprocess.run(['traceroute', ip_v4],capture_output=True,text=True,encoding='cp866')
    return route.stdout, route.returncode

def traceroute6(ip_v6):
    route = subprocess.run(['traceroute6', ip_v6],capture_output=True,text=True,encoding='cp866')
    return route.stdout, route.returncode
# arr = ["google.com", "ya.ru", "e.mail.ru", "github.com",
#        "youtube.com", "vk.com", "leetcode.com", "classroom.google.com", "www.ozon.ru"]
arr = ["google.com"]

data={
    "домен" : [],
    "ip для traceroute" : [],
    "ip узла" : [],
    "время первого запроса" : [],
    "время второго запроса" : [],
    "время третьего запроса" : []
    }


for host in arr:
    ipv4, code_ipv4, ipv6, code_ipv6 = dig(host)
    # print(f"v4 for{host}",ipv4)
    # print(f"v6 for{host}", ipv6)
    if not code_ipv4 and ipv4:
        for ip in ipv4:
            print(ip)
            # route, code = traceroute(ip)
            # print(route)
    if not code_ipv6 and ipv6:
        for ip in ipv6:
            print(ip)
            # route, code = traceroute6(ip)
            # print(route)


# df = pd.DataFrame(data)
# df.to_csv("1.csv", index=False)