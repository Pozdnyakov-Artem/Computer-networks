import re
import subprocess

import pandas as pd


def dig(host):
    ipv4 = subprocess.run(['dig', host, '+short'],capture_output=True,text=True,encoding='cp866')
    ipv6 = subprocess.run(['dig', 'AAAA', host, '+short'], capture_output=True, text=True, encoding='cp866')
    return ipv4.stdout, ipv4.returncode, ipv6.stdout, ipv6.returncode

arr = ["google.com", "ya.ru", "e.mail.ru", "chat.deepseek.com","github.com",
       "youtube.com", "vk.com", "leetcode.com", "classroom.google.com", "www.ozon.ru"]


for host in arr:
    ipv4, code_ipv4, ipv6, code_ipv6 = dig(host)
    print(f"v4 for{host}",ipv4)
    print(f"v6 for{host}", ipv6)


# df = pd.DataFrame(data)
# df.to_csv("1.csv", index=False)