import re
import subprocess

import pandas as pd


def dig(host):
    ipv4 = subprocess.run(['dig', host, '+short'],capture_output=True,text=True,encoding='cp866')
    ipv6 = subprocess.run(['dig', 'AAAA', host, '+short'], capture_output=True,encoding='cp866')
    return ipv4.stdout, ipv4.returncode, ipv6.stdout, ipv6.returncode

def traceroute(ip_v4):
    route = subprocess.run(['traceroute', ip_v4],capture_output=True,text=True,encoding='cp866')
    return route.stdout, route.returncode

def traceroute6(ip_v6):
    route = subprocess.run(['traceroute6', ip_v6],capture_output=True,text=True,encoding='cp866')
    return route.stdout, route.returncode
#arr = ["google.com", "ya.ru", "e.mail.ru", "github.com",
#        "youtube.com", "vk.com", "leetcode.com", "classroom.google.com", "www.>
arr = ["youtube.com"]

data={
    "домен" : [],
    "ip_версия" : [],
    "ip для traceroute" : [],
    "номер узла" : [],
    "ip узла" : [],
    "время первого запроса" : [],
    "время второго запроса" : [],
    "время третьего запроса" : []
    }

def add_to_data(domen, ip, ip_version, route):
    # print(len(route))
    bias = 0 if ip == "v4" else 1
    route = route.splitlines() #[:-1]
    # print(route)
    for idx, line in enumerate(route):
        if idx == 0 or line.count('*') == 3:
            continue
        line = line.split()
        line = [word for word in line if word != "ms"]
        # print(idx, line)
        data["домен"].append(domen)
        data["ip_версия"].append(ip_version)
        data["ip для traceroute"].append(ip)
        data["номер узла"].append(line[0])
        data["ip узла"].append(line[1])
        data["время первого запроса"].append(line[2+bias])
        data["время второго запроса"].append(line[3+bias])
        data["время третьего запроса"].append(line[4+bias])


for host in arr:
    ipv4, code_ipv4, ipv6, code_ipv6 = dig(host)
    ipv4 = ("".join(ipv4)).splitlines()
    ipv6 = ("".join(ipv6)).splitlines()

    if not code_ipv4 and ipv4:
        for ip in ipv4:
            print(ip)
            route, code = traceroute(ip)
            if not code:
                add_to_data(host, ip, "v4", route)
    if not code_ipv6 and ipv6:
        for ip in ipv6:
            print(ip)
            route, code = traceroute6(ip)
            if not code:
                add_to_data(host, ip, "v6", route)


df = pd.DataFrame(data)
df.to_csv("1.csv", index=False)

