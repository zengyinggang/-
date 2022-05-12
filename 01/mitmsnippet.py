from mitmproxy import ctx

class RemoveJS:
    def response(self, flow):
        if flow.request.url == "http://match.yuanrenxue.com/static/match/safety/uzt.js" or \
            flow.request.url == "http://match.yuanrenxue.com/static/match/safety/uyt.js":
            flow.response.set_text("")

addons = [
    RemoveJS(),
]