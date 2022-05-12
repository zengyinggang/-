from io import BytesIO
from fontTools.ttLib import TTFont
import requests
import base64

def make_standard():
    # 设置标准
    # font = TTFont("./font.woff")
    # font.saveXML("xml_font.xml")

    # 利用on是否一样判断是否是一样的数字
    font = TTFont("./font.woff")
    standard_order = [0, 9, 6, 7, 3, 1, 2, 4, 5, 8]
    standard_items = font.getGlyphSet()
    font_names = font.getGlyphNames()

    # 组合成字典
    standard_result_dict = {}
    for index, name in enumerate(font_names[1:]):
        # 获取标准woff里面的on值
        # item_on = list(standard_items[name]._glyph.flags)
        item_on = list(font['glyf'][name].flags)
        # 组合
        number = standard_order[index]
        standard_result_dict[number] = item_on

    # print(standard_result_dict)
    return standard_result_dict

def make_relation(file_, cmp):
    """利用上面函数得到的标准关系，然后生成一个xml文件对on值看是那一个函数，最后return 一个对应的函数字典

    Args:
        file (bytes): 需要生成一个xml文件
    """
    font = TTFont(BytesIO(file_))

    items = font.getGlyphSet()
    names = font.getGlyphNames()

    cmp_dict = {}
    for index, name in enumerate(names[1:]):
        flag = list(font['glyf'][name].flags)
        for key, value in cmp.items():
            if value == flag:
                cmp_dict[name] = key
    return cmp_dict

def make_request():

    """发送请求
    """

    url = 'http://match.yuanrenxue.com/api/match/7'

    names = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖', '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀', '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮', '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子', '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚', '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']
    print("一共%s" % len(names))

    yyq = 1
    img_num = 1
    imgnum_arr = [1, 8, 3, 2, 4, 5, 7, 5, 15, 3, 9, 8, 5, 1, 3]
    level_arr = [1, 4, 3, 2, 9, 15]

    cmp = make_standard()

    for page_number in range(1, 6):
        resp = requests.get(url=url, params={"page":page_number}, headers=headers)
        # 请求错误
        if resp.status_code == 400:
            raise ValueError("404 错粗")

        # 请求正常
        else:
            data = resp.json()
            woff = data["woff"]
            # 直接写入内存
            after_base64 = base64.b64decode(woff.encode("utf-8"))
            # 拿到对应关系
            match_result = make_relation(after_base64, cmp)
            match_result = {k.replace("uni", ""):v for k, v in match_result.items()}
            value_list = data["data"]
            # 开始重写JS
            for num in value_list:
                # 名称
                name = names[yyq]
                # 数字
                number = num["value"]
                number_list = number.split(" ")
                decode_number = ''
                for i in number_list:
                    if i != '':
                        n = i[3:]
                        n = match_result[n]
                        decode_number += str(n)
                yyq += 1
                total.append((name, int(decode_number)))


headers = {
    'Proxy-Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'yuanrenxue.project',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://match.yuanrenxue.com/match/7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
total = list()
make_request()
total.sort(key=lambda x:x[1])
print(total)