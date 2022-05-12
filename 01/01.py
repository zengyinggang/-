import requests
import time
import execjs
from bs4 import BeautifulSoup
import json

raw_header = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1625246590; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1625246592; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1625246973; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1625247153
Host: match.yuanrenxue.com
Pragma: no-cache
Referer: http://match.yuanrenxue.com/match/1
User-Agent: yuanrenxue.project 
X-Requested-With: XMLHttpRequest
"""

header = {i.split(':', maxsplit=1)[0].strip():i.split(':', maxsplit=1)[1].strip() for i in raw_header.split('\n') if i != ''}


def get_m():
    js_env = execjs.get()
    with open("./01.js") as f:
        file = f.read()
    ctx = js_env.compile(file)
    m = ctx.call("get_m", int(time.time() + 100000))
    m = m.replace("丨", "%E4%B8%A8")
    return m

def page(page, m):
    url = "http://match.yuanrenxue.com/api/match/1?page={}&m={}".format(page, m)
    resp = requests.get(url, headers=header, proxies={"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"})
    value = resp.json()
    return value

value_list = []
for i in range(1, 6):
    page_value = page(i, get_m())
    per_page_value = page_value["data"]
    for p in per_page_value:
        value_list.append(p["value"])

average = 0
number = len(value_list)
for v in value_list:
    average += v
average = average / number
print(average)