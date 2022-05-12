import requests
import execjs
from requests import status_codes

raw_header = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: match.yuanrenxue.com
Pragma: no-cache
Referer: http://match.yuanrenxue.com/match/5
User-Agent: yuanrenxue.project 
X-Requested-With: XMLHttpRequest
"""


# class Question5:
#     def __init__(self):
#         self.file = None
#         self.headers = None
#         self.url = "http://match.yuanrenxue.com/api/match/5"

#     def make_header(self, raw_headers):
#         my_headers = {i.split(":", maxsplit=1)[0].strip(): i.split(":", maxsplit=1)[1].strip() for i in raw_headers.split("\n") if i != ''}
#         self.headers = my_headers

#     def update_cookie(self):
#         Cookie = {}
#         data = {"RM4hZBv0dDon443M": self.file["RM4hZBv0dDon443M"], "m":self.file["m_md5"]}
#         Cookie.update(data)
#         self.headers = Cookie

#     def make_encrypt_value(self):
#         with open("./run.js") as f:
#             file = f.read()
#         js_env = execjs.get()
#         ctx = js_env.compile(file)
#         result = ctx.call("get_cookies")
#         self.file = dict(result)

#     def request_page(self, page_number):
#         if page_number == 1:
#             res = requests.get(
#                 self.url,
#                 # headers=self.headers,
#                 # params={"page": page_number, "f": self.file["f"]-1000000, "m":self.file["m"]-1000000},
#             )
#             print("ok")
#             print(res.json())
#             return res.json()
#         else:
#             self.make_encrypt_value()
#             self.update_cookie()
#             print(self.headers)
#             res = requests.get(
#                 self.url,
#                 headers=self.headers,
#                 params={"page": page_number, "f": int(self.file["f"]), "m":int(self.file["m"])},
#             )
#             print(res.text)
#             print(res.url)
#             return res.text

#     def full_list(self, data, list_):
#         if isinstance(data, dict) & isinstance(list_, list):
#             list_.append(data["data"])
#         else:
#             raise ValueError("获取的数据有问题%s, 或则传入的list错误" % data)


# def main():
#     values = []
#     question = Question5()
#     question.make_header(raw_header)
#     for number in range(1, 3):
#         data = question.request_page(number)
#         question.full_list(data, values)
#     print(values)

# main()

def run_js():
    with open("./run.js") as f:
        file = f.read()
    js_env = execjs.get()
    ctx = js_env.compile(file)
    result = ctx.call("get_cookies")
    return result

def get_page(number):
    js_result = run_js()
    url = "http://match.yuanrenxue.com/api/match/5"
    my_headers = {i.split(":", maxsplit=1)[0].strip(): i.split(":", maxsplit=1)[1].strip() for i in raw_header.split("\n") if i != ''}
    res = requests.get(url, headers=my_headers, 
        cookies={"RM4hZBv0dDon443M":js_result["RM4hZBv0dDon443M"],"m":js_result["m_md5"]},
        params={"page":number, "m": js_result["m"], "f": js_result["f"]}
    )
    # 如果在请求中出现cookie过期
    if res.status_code == 400:
        js_result_2 = run_js() 
        print("J2", js_result_2)
        res = requests.get(url, headers=my_headers, 
        cookies={"RM4hZBv0dDon443M":js_result["RM4hZBv0dDon443M"],"m":js_result["m_md5"]},
        params={"m": js_result["m"], "f": js_result["f"]}
        )
        # 请求成功继续请求之前的页码
        if res.status_code == 200:
            res = requests.get(url, headers=my_headers, 
            cookies={"RM4hZBv0dDon443M":js_result_2["RM4hZBv0dDon443M"],"m":js_result_2["m_md5"]},
            params={"page":number, "m": js_result_2["m"], "f": js_result_2["f"]}
            )
            # print("S2", res.text)
            return res.json()
    else:
        # print(res.js)
        # print("S1", res.text)
        return res.json()

values = []
for i in range(1, 6):
    data = get_page(i)
    values.append(data["data"])

numbers = []
for i in values:
    for x in i :
        numbers.append(x["value"])

numbers.sort(reverse=True)

result = numbers[0:5]
total = 0
for i in result:
    total += i
print(total)