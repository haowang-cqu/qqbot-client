import requests


def dog() -> str:
    """获取舔狗日记
    """
    resp = requests.get(url="http://lkaa.top/API/tgrj/api.php")
    if resp.status_code == 200:
        return resp.text;
    else:
        return "今天就不当舔狗了"
