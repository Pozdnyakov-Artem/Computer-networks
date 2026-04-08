import re
import subprocess

import pandas as pd


def dig(host):
    ipv4 = subprocess.run(['dig', host, '+short'],capture_output=True,text=True,encoding='cp866')
    ipv6 = subprocess.run(['dig', 'AAAA', host, '+short'], capture_output=True, text=True, encoding='cp866')
    return ipv4.stdout, ipv4.returncode, ipv6.stdout, ipv6.returncode

def take_ip(line,data):
    if "Обмен" in line:
        data["ip"].append(re.search(r"\[([\d\.]+)\]",line).group(1))

def take_tll(line,arr_ttl):
    if "Ответ" in line:
        arr_ttl.append(int(re.search(r"TTL=(\d+)",line).group(1)))

def losses(line,data):
    if "потерь" in line:
        data["процент потерь"].append((re.search(r"(\d+)%", line).group(1)))



arr = ["google.com", "ya.ru", "e.mail.ru", "chat.deepseek.com","github.com",
       "youtube.com", "vk.com", "leetcode.com", "classroom.google.com", "www.ozon.ru"]


for host in arr:
    ipv4, code_ipv4, ipv6, code_ipv6 = dig(host)
    print(*ipv4, *ipv6)


# df = pd.DataFrame(data)
# df.to_csv("1.csv", index=False)