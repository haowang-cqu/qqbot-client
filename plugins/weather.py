import requests
from datetime import date
from .secret import secret


def weather(city="重庆", cityid=None):
    """天气API
    website: https://tianqiapi.com/index/doc?version=v61
    """
    query = {
        "appid": secret['weather']['appid'],
        "appsecret": secret['weather']['appsecret'],
        "version": "v61",
        "city": city,
        "cityid": cityid
    }
    resp = requests.get(
        url="https://v0.yiketianqi.com/api",
        params=query
    )
    if resp.status_code == 200:
        data = resp.json()
        if "errcode" in data:
            return None
        else:
            return data
    else:
        return None


def format_weather(city="重庆"):
    """格式化天气信息
    """
    data = weather(city=city)
    if not data:
        return None
    weather_icon = {
        "bingbao": "🌨️",
        "lei": "🌩️",
        "leizhenyu": "⛈️",
        "qing": "☀️",
        "shachen": "🌪️",
        "wu": "🌫️",
        "xue": "🌨️",
        "yin": "⛅",
        "yu": "🌧️",
        "yun": "☁️"
    }
    icon = ""
    if data['wea_img'] in weather_icon:
        icon = weather_icon[data['wea_img']]
    message  =  f"{data['city']} 【{data['wea']} {icon}】\n"\
                f"气温: {data['tem']}℃ ↑{data['tem1']}↓{data['tem2']}\n"\
                f"风力: {data['win']}{data['win_speed']}\n"\
                f"空气质量: {data['air']}/{data['air_level']}\n"
    # 预警信号
    alarm = False
    if 'alarm' in data and len(data['alarm']['alarm_type']):
        alarm = True
        message += f"🚨{data['alarm']['alarm_type']}{data['alarm']['alarm_level']}预警\n"
        message += f"{data['alarm']['alarm_content']}\n"
    # 没有预警的情况下打印空气质量提醒
    if not alarm:
        message += f"{data['air_tips']}\n"
    message += "--------------\n"
    message += f"更新时间: {data['update_time']}"
    return message
