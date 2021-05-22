import time
import requests
import hashlib
import random
import uuid
from .secret import secret


lang_command = {
    "翻译": "zh-CHS",
    "中文": "zh-CHS",
    "汉语": "zh-CHS",
    "英文": "en",
    "英语": "en",
    "日文": "ja",
    "日语": "ja",
    "韩文": "ko",
    "韩语": "ko",
    "法文": "fr",
    "法语": "fr",
    "西班牙文": "es",
    "西班牙语": "es",
    "葡萄牙文": "pt",
    "葡萄牙语": "pt",
    "意大利文": "it",
    "意大利语": "it",
    "俄文": "ru",
    "俄语": "ru",
    "越南文": "vi",
    "德文": "de",
    "德语": "de",
    "阿拉伯文": "ar",
    "印尼文": "id",
    "南非荷兰语": "af",
    "波斯尼亚语": "bs",
    "保加利亚语": "bg",
    "粤语": "yue",
    "加泰隆语": "ca",
    "克罗地亚语": "hr",
    "捷克语": "cs",
    "丹麦语": "da",
    "荷兰语": "nl",
    "爱沙尼亚语": "et",
    "斐济语": "fj",
    "芬兰语": "fi",
    "希腊语": "el",
    "海地克里奥尔语": "ht",
    "希伯来语": "he",
    "印地语": "hi",
    "白苗语": "mww",
    "匈牙利语": "hu",
    "斯瓦希里语": "sw",
    "克林贡语": "tlh",
    "拉脱维亚语": "lv",
    "立陶宛语": "lt",
    "马来语": "ms",
    "马耳他语": "mt",
    "挪威语": "no",
    "波斯语": "fa",
    "波兰语": "pl",
    "克雷塔罗奥托米语": "otq",
    "罗马尼亚语": "ro",
    "塞尔维亚语(西里尔文)": "sr-Cyrl",
    "塞尔维亚语(拉丁文)": "sr-Latn",
    "斯洛伐克语": "sk",
    "斯洛文尼亚语": "sl",
    "瑞典语": "sv",
    "塔希提语": "ty",
    "泰语": "th",
    "汤加语": "to",
    "土耳其语": "tr",
    "乌克兰语": "uk",
    "乌尔都语": "ur",
    "威尔士语": "cy",
    "尤卡坦玛雅语": "yua",
    "阿尔巴尼亚语": "sq",
    "阿姆哈拉语": "am",
    "亚美尼亚语": "hy",
    "阿塞拜疆语": "az",
    "孟加拉语": "bn",
    "巴斯克语": "eu",
    "白俄罗斯语": "be",
    "宿务语": "ceb",
    "科西嘉语": "co",
    "世界语": "eo",
    "菲律宾语": "tl",
    "弗里西语": "fy",
    "加利西亚语": "gl",
    "格鲁吉亚语": "ka",
    "古吉拉特语": "gu",
    "豪萨语": "ha",
    "夏威夷语": "haw",
    "冰岛语": "is",
    "伊博语": "ig",
    "爱尔兰语": "ga",
    "爪哇语": "jw",
    "卡纳达语": "kn",
    "哈萨克语": "kk",
    "高棉语": "km",
    "库尔德语": "ku",
    "柯尔克孜语": "ky",
    "老挝语": "lo",
    "拉丁语": "la",
    "卢森堡语": "lb",
    "马其顿语": "mk",
    "马尔加什语": "mg",
    "马拉雅拉姆语": "ml",
    "毛利语": "mi",
    "马拉地语": "mr",
    "蒙古语": "mn",
    "缅甸语": "my",
    "尼泊尔语": "ne",
    "齐切瓦语": "ny",
    "普什图语": "ps",
    "旁遮普语": "pa",
    "萨摩亚语": "sm",
    "苏格兰盖尔语": "gd",
    "塞索托语": "st",
    "修纳语": "sn",
    "信德语": "sd",
    "僧伽罗语": "si",
    "索马里语": "so",
    "巽他语": "su",
    "塔吉克语": "tg",
    "泰米尔语": "ta",
    "泰卢固语": "te",
    "乌兹别克语": "uz",
    "南非科萨语": "xh",
    "意第绪语": "yi",
    "约鲁巴语": "yo",
    "南非祖鲁语": "zu"
}


def translation_youdao(text: str, to_lang: str, from_lang: str="auto") -> str:
    """有道
    website: https://ai.youdao.com/
    """
    app_id = secret["youdao"]["app_id"]
    app_key = secret["youdao"]["app_key"]
    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    sign = hashlib.sha256((app_id + truncate(text) + salt + curtime + app_key).encode(encoding="utf-8")).hexdigest()
    data = {
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appKey": app_id,
        "signType": "v3",
        "curtime": curtime,
        "salt": salt,
        "sign": sign
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = "https://openapi.youdao.com/api"
    resp = requests.post(url=url, data=data, headers=headers)
    if resp.status_code == 200:
        ret_data = resp.json()
        if ret_data["errorCode"] != "0":
            return None
        result = ""
        if ret_data["l"] == "en2zh-CHS" and "basic" in ret_data:
            basic = ret_data["basic"]
            result += ret_data["query"] + "\n"
            if "uk-phonetic" in basic and "us-phonetic" in basic:
                result += f"英[{basic['uk-phonetic']}] 美[{basic['us-phonetic']}]\n"
            if "explains" in basic:
                result += "\n".join(basic['explains']) + "\n"
            if "wfs" in basic:
                for wf in basic["wfs"]:
                    result += wf["wf"]["name"] + " " + wf["wf"]["value"] + ";"
        else:
            result += ret_data["translation"][0]
        return result
    else:
        return None


class Youdao():
    """有道翻译类
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
          }
        self.data = {
            'i': None,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': None,
            'sign': None,
            'ts': None,
            'bv': None,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
          }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    def translate(self, word):
        ts = str(int(time.time()*10000))
        salt = str(int(time.time()*10000)) + str(int(random.random()*10))
        sign = 'fanyideskweb' + word + salt + '97_3(jkMYg@T[KZQmqjTK'
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['ts'] = ts
        self.data['bv'] = bv
        res = requests.post(self.url, headers=self.headers, data=self.data)
        print(res.json())
        return [res.json()['translateResult'][0][0].get('tgt')]