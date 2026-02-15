import re
import subprocess

import pandas as pd


def ping(host):
    result = subprocess.run(['ping','-n', '3', host],capture_output=True,text=True,encoding='cp866')
    return result.stdout, result.returncode

def take_ip(line,data):
    if "Обмен" in line:
        data["ip"].append(re.search(r"\[([\d\.]+)\]",line).group(1))

def take_tll(line,arr_ttl):
    if "Ответ" in line:
        arr_ttl.append(int(re.search(r"TTL=(\d+)",line).group(1)))

def losses(line,data):
    if "потерь" in line:
        data["процент потерь"].append((re.search(r"(\d+)%", line).group(1)))

def take_data(line,data):
    if "Минимальное" in line:
        words = line.split()
        data["домен"].append(host)
        data["прием-передача мин"].append(re.search(r"(\d+)мсек", words[2]).group(1))
        data["прием-передача ср"].append(words[9])
        data["прием-передача макс"].append(words[5])


arr = ["google.com", "ya.ru", "e.mail.ru", "chat.deepseek.com","github.com",
       "youtube.com", "vk.com", "leetcode.com", "classroom.google.com", "www.ozon.ru"]

data={
    "домен" : [],
    "ip" : [],
    "TTL" : [],
    "прием-передача мин" : [],
    "прием-передача ср" : [],
    "прием-передача макс" : [],
    "процент потерь" : []
    }

for host in arr:
    lines, code = ping(host)
    arr_ttl = []
    if not code:
        for line in lines.split('\n'):
            take_ip(line,data)
            take_tll(line,arr_ttl)
            take_data(line,data)
            losses(line,data)
        data["TTL"].append(sum(arr_ttl) / len(arr_ttl))
    else:
        data["домен"].append(host)
        data["TTL"].append(None)
        data["прием-передача мин"].append(None)
        data["прием-передача ср"].append(None)
        data["прием-передача макс"].append(None)
        for line in lines.split('\n'):
            losses(line, data)
            take_ip(line, data)

df = pd.DataFrame(data)
df.to_csv("1.csv", index=False)