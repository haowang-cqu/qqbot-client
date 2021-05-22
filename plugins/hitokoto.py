import requests


def hitokoto() -> str:
    """一言API
    """
    resp = requests.get(url="https://v1.hitokoto.cn?encode=text")
    if resp.status_code == 200:
        return resp.text
    else:
        return "用代码表达言语的魅力，用代码书写山河的壮丽。"