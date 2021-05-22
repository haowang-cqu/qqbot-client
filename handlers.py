"""
上报事件处理
"""
from models import *
from api import *
from plugins.dog import dog
from plugins.hitokoto import hitokoto
from plugins.weather import format_weather
from plugins.music import get_music_id
from plugins.search import zhihu
from plugins.qr import get_qr
from plugins.translation import translation_youdao, lang_command


def private_message_handler(event: Event):
    """处理私聊消息
    """
    user_id = event.user_id
    message = event.message
    print(f"私聊消息: 【{user_id}】说【{message}】")
    if "ping" == message:
        send_private_msg(user_id, "pong")
        return
    if "舔狗日记" == message:
        send_private_msg(user_id, dog())
        return
    if message in ("一言", "骚话", "名言"):
        send_private_msg(user_id, hitokoto())
        return

    command = message.split()[0]

    if command in ("天气", "weather"):
        if len(message.split()) == 1:
            wea = format_weather()
        else:
            wea = format_weather(message.split()[1])
        if wea:
            send_private_msg(user_id, wea)
        return

    if command in ("点歌", "网易云音乐", "网易云", "网抑云", "music"):
        keywords = message[len(command)+1:]
        music_id = get_music_id(keywords, "163")
        if music_id:
            send_private_msg(user_id, f"[CQ:music,type=163,id={music_id}]")
        return

    if command in ("qq音乐", "QQ音乐", "Qq音乐", "qQ音乐", "Q音", "q音"):
        keywords = message[len(command)+1:]
        music_id = get_music_id(keywords, "qq")
        if music_id:
            send_private_msg(user_id, f"[CQ:music,type=qq,id={music_id}]")
        return

    if command in ("知乎", "zhihu"):
        keywords = message[len(command)+1:]
        data = zhihu(keywords)
        if data:
            send_private_msg(user_id, f"[CQ:share,url={data['url']},title={data['title']},content={data['content']},image={data['image']}]")
        return

    if command in ("二维码", "qr", "qrcode"):
        data = message[len(command)+1:]
        send_private_msg(user_id, f"[CQ:image,file=base64://{get_qr(data)}]")
        return

    # 处理翻译
    if command in lang_command:
        result = translation_youdao(message[len(command)+1:], to_lang=lang_command[command])
        if result:
            send_private_msg(user_id, result)
        return


def group_message_handler(event: Event):
    """处理群聊消息
    """
    group_id = event.group_id
    user_id = event.user_id
    message = event.message
    print(f"群聊消息：【{group_id}】中【{user_id}】说【{message}】")
    if "ping" == message:
        send_group_msg(group_id, f"[CQ:at,qq={user_id}]pong")
        return
    if "舔狗日记" == message:
        send_group_msg(group_id, f"[CQ:at,qq={user_id}]{dog()}")
        return
    if message in ("一言", "骚话", "名言"):
        send_group_msg(group_id, f"[CQ:at,qq={user_id}]{hitokoto()}")
        return
    
    command = message.split()[0]

    if command in ("天气", "weather"):
        if len(message.split()) == 1:
            wea = format_weather()
        else:
            wea = format_weather(message.split()[1])
        if wea:
            send_group_msg(group_id, wea)
        return

    if command in ("点歌", "网易云", "网抑云", "music"):
        keywords = message[len(command)+1:]
        music_id = get_music_id(keywords, "163")
        if music_id:
            send_group_msg(group_id, f"[CQ:music,type=163,id={music_id}]")
        return

    if command in ("qq音乐", "QQ音乐", "Qq音乐", "qQ音乐", "Q音", "q音"):
        keywords = message[len(command)+1:]
        music_id = get_music_id(keywords, "qq")
        if music_id:
            send_group_msg(group_id, f"[CQ:music,type=qq,id={music_id}]")
        return

    if command in ("知乎", "zhihu"):
        question = message[len(command)+1:]
        data = zhihu(question)
        if data:
            send_group_msg(group_id, f"[CQ:share,url={data['url']},title={data['title']},content={data['content']},image={data['image']}]")
        return

    if command in ("二维码", "qr", "qrcode"):
        data = message[len(command)+1:]
        send_group_msg(group_id, f"[CQ:at,qq={user_id}][CQ:image,file=base64://{get_qr(data)}]")
        return

    # 处理翻译
    if command in lang_command:
        result = translation_youdao(message[len(command)+1:], to_lang=lang_command[command])
        if result:
            send_group_msg(group_id, f"[CQ:at,qq={user_id}]{result}")
        return


def event_handler(event: Event):
    """事件分发
    """
    if event.post_type == PostType.message and event.message_type == MessageType.private:
        private_message_handler(event)
    elif event.post_type == PostType.message and event.message_type == MessageType.group:
        group_message_handler(event)
    elif event.post_type == PostType.meta_event:
        print(event.json(exclude_unset=True, exclude_none=True))