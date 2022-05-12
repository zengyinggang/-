import requests
from fontTools.ttLib import TTFont
from io import BytesIO
import base64
def parseByFlag(fontfile):
    #选定一个基准参照，确定flag和数字的关系
    font = TTFont("./font.woff")
    gs = font.getGlyphSet()
    glyphNames = font.getGlyphNames()

    #这个数字顺序跟xml里的TTGlyph name顺序是一致的
    num_list = [4,6,9,0,2,8,1,5,3,7]
    map_dict={}

    for i,name in enumerate(glyphNames[1:]):
        g = gs[name]
        flag = list(g._glyph.flags)#读取每个坐标对应的on值
        # coord=g._glyph.coordinates#获取每个字符的坐标序列

        #字典里的键对应的数字，值则是on值构成的列表
        map_dict[num_list[i]]=flag

    # print('标准对应关系为：',map_dict)



    font = TTFont(BytesIO(fontfile))#待解析字体文件
    gs = font.getGlyphSet()
    glyphNames = font.getGlyphNames()
    list2=[]
    for i,name in enumerate(glyphNames[1:]):
        g = gs[name]
        flag = list(g._glyph.flags)#读取每个坐标对应的on值

        for key,value in map_dict.items():
            if value==flag:
                list2.append((name,key))

    # print('解析后的数字对应关系：')
    # for m in list2:
    #     print(m)

    return list2

def get_parseResult():
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'yuanrenxue.project',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://match.yuanrenxue.com/match/7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    name = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖',
            '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀',
            '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮',
            '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子',
            '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚',
            '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']

    player_dict = {}

    for i in range(1,6):
        map_dict={}
        page=i
        params = (
            ('page', str(page)),
        )

        response = requests.get('http://match.yuanrenxue.com/api/match/7', headers=headers, params=params)
        data=response.json()
        woff=data['woff']
        valuelist = data['data']

        fontfile = base64.b64decode(woff.encode())
        match_result=parseByFlag(fontfile)

        match_result=[(l[0].replace('uni','&#x'),l[1]) for l in match_result]
        map_dict={}
        for m in match_result:
            map_dict[m[0]]=str(m[1])

        for n, v in enumerate(valuelist):
            # 解析得到胜点值
            win_point = v['value'].split(' ')
            del win_point[-1]
            real_win_point = [map_dict[num] for num in win_point]
            str_ = ''
            real_win_point = str_.join(real_win_point)
            print(real_win_point)

            # 将玩家与胜点值关联
            player = name[(n + 1) + (page - 1) * 10]

            player_dict[player] = int(real_win_point)

        for key, value in player_dict.items():
            print(key, value)


get_parseResult()