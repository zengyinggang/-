# 猿人学第九题

import requests
import execjs
import re

def run_js(time):
    with open("./09.js") as f:
        file = f.read()
    js_env = execjs.get()
    ctx = js_env.compile(file)
    result = ctx.call("get_m", time)
    return result

my_headers = """
cache-control:	max-age=0
sec-ch-ua:	"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile:	?0
upgrade-insecure-requests:	1
user-agent:	yuanrenxue.project
accept:	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
sec-fetch-site:	same-origin
sec-fetch-mode:	navigate
sec-fetch-user:	?1
sec-fetch-dest:	document
referer:	https://match.yuanrenxue.com/match/9
accept-encoding:	gzip, deflate, br
accept-language:	zh-CN,zh;q=0.9
"""

my_headers = {i.split(":", maxsplit=1)[0].strip(): i.split(":", maxsplit=1)[1].strip() for i in my_headers.split("\n") if i != ''}
my_cookies = {'cookie': 'Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1628729841; no-alert3=true; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1628729844; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1628729844; sessionid=6h9exxhjrfa3sgbuqrfsxe4qe94cy2op; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1628867811'}

def get_page(page):
    session = requests.session()
    my_url = "https://match.yuanrenxue.com/api/match/9"
    res = session.get(
        my_url,
        headers=my_headers,
        cookies=my_cookies,
        params={"page": page}
    )
    if res.status_code == 200:
        print("ok")
        print(res.text)
    else:
        # get timestamp
        my_url_erro = "https://match.yuanrenxue.com/match/9"
        res = session.get(
            my_url_erro,
            headers=my_headers,
        )
        timestamp = re.search(r"decrypt,'([0-9]+)'", res.text).group(1)
        m = run_js(str(timestamp))
        # 再次请求带上m
        # print(session.cookies.values)
        res = session.get(
            my_url,
            headers=my_headers,
            cookies={"m":m},
            params={"page": page}
        )
        print(res.text)
        return res.json()

data_list = []
for i in range(1,6):
    data = get_page(i)["data"]
    for d in data:
        data_list.append(d["value"])

print(data_list)
count = len(data_list)
al = sum(data_list)
average = al/count
print(average)