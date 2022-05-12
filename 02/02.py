import execjs
import requests

raw = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Cookie: Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1625393144; qpfccr=true; no-alert3=true; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1625394820;
Host: match.yuanrenxue.com
Pragma: no-cache
Proxy-Connection: keep-alive
Referer: http://match.yuanrenxue.com/match/2
User-Agent: yuanrenxue.project 
X-Requested-With: XMLHttpRequest
"""

class Practice:
    def __init__(self) -> None:
        self.url = "http://match.yuanrenxue.com/api/match/2"

    def make_header(self, raw_header):
        self.header = {i.split(':', maxsplit=1)[0].strip():i.split(':', maxsplit=1)[1].strip() for i in raw_header.split('\n') if i != ''}

    def read_file(self, file="./02.js"):
        env_js = execjs.get()
        with open(file, "r") as f:
            file = f.read()
        ctx = env_js.compile(file)
        return ctx

    def run_js(self):
        ctx = self.read_file()
        value = ctx.call("get_cookies")
        return value

    def update_cookie(self):
        cookie_value = self.header["Cookie"]
        cookie_value = cookie_value + self.run_js()
        self.header.update({"Cookie": cookie_value})

    def get_page(self, page, update=False):
        if update is False:
            resp = requests.get(self.url, headers=self.header, params={"page": page})
            if resp.status_code == 400:
                print("cookie 过期")
                return self.get_page(page, update=True)
            else:
                return resp.json()
        else:
            new_header = self.update_cookie()
            resp = requests.get(self.url, headers=self.header)
            return resp.json()

    def make_average(self):
        pass

value_list = []

exam = Practice()
exam.make_header(raw)
for i in range(1, 6):
    values = exam.get_page(i)
    for x in values["data"]:
        value_list.append(x["value"])

average = 0
for i in value_list:
    average += i
print(average)