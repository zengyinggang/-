import requests
import execjs

chrome_headers = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1626325085; qpfccr=true; no-alert3=true; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1626325088; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1626325088; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1626325368
Host: match.yuanrenxue.com
Pragma: no-cache
Referer: http://match.yuanrenxue.com/match/6
User-Agent: yuanrenxue.project
X-Requested-With: XMLHttpRequest
"""

class Question:
    def __init__(self):
        self.request_times = 1
        self.b_data = ''
        self.timestamp = None
        self.headers = None
        self.encrypt_data_m = None

    def make_headers(self, raw_headers):
        headers = {i.split(":", maxsplit=1)[0].strip(): i.split(":", maxsplit=1)[1].strip() for i in raw_headers.split("\n") if i != ''}
        self.headers = headers

    def run_js_timestamp(self,):
        with open("./06.js") as f:
            file = f.read()
        js_env = execjs.get()
        ctx = js_env.compile(file)
        result = ctx.call("get_timestamp")
        self.timestamp = result
        return result

    def run_js_get_q(self,):
        with open("./06.js") as f:
            file = f.read()
        js_env = execjs.get()
        ctx = js_env.compile(file)
        result = ctx.call("make_q", self.b_data, self.timestamp, self.request_times)
        self.b_data = result
        return result

    def run_js_get_encrypt(self,):
        with open("./06.js") as f:
            file = f.read()
        js_env = execjs.get()
        ctx = js_env.compile(file)
        result = ctx.call("encrypt", self.timestamp, self.request_times)
        self.encrypt_data_m = result
        return result

    def request(self, murl, mpage_number, mparams):
        update_params = {"page": mpage_number}
        update_params.update(mparams)
        res = requests.get(
            url=murl,
            headers=self.headers,
            params=update_params,
        )
        self.request_times += 1
        return res.json()

def main():
    numbers = []
    for i in range(1, 6):
        url = "http://match.yuanrenxue.com/api/match/6"
        q = Question()
        q.make_headers(chrome_headers)

        t = q.run_js_timestamp()

        rq = q.run_js_get_q()

        m = q.run_js_get_encrypt()

        data = q.request(url, i, {"m":m, "q":rq})
        for d in data["data"]:
            numbers.append(d["value"]*8)
            numbers.append(d["value"]*15)
            numbers.append(d["value"])
    print(numbers)
    total = 0
    for i in numbers:
        total += i
    print(total)

main()