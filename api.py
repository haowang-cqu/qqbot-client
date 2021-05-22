"""
调用机器人的公开API
"""
import requests
from models import MessageType
from typing import Optional

base_url = "http://iamwh.cn:5700"


def send_private_msg(user_id: int, message: str, auto_escape: bool=False) -> int:
    """发送私聊消息
    """
    endpoint = "/send_private_msg"
    resp = requests.get(
        url=base_url+endpoint,
        params= {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape
        },
        timeout=5
    )
    return resp.status_code


def send_group_msg(group_id: int, message: str, auto_escape: bool=False) -> int:
    """发送群消息
    """
    endpoint = "/send_group_msg"
    resp = requests.get(
        url=base_url+endpoint,
        params= {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        },
        timeout=5
    )
    return resp.status_code
    

def send_msg(message: str, auto_escape: bool=False, message_type: MessageType = None,\
    user_id: int = None, group_id: int = None) -> int:
    """发送消息
    """
    endpoint = "/send_msg"
    resp = requests.get(
        url=base_url+endpoint,
        params= {
            "message_type": message_type,
            "user_id": user_id,
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        },
        timeout=5
    )
    return resp.status_code


def clean_cache() -> int:
    """清理缓存
    """
    endpoint = "/clean_cache"
    resp = requests.get(
        url=base_url+endpoint,
        timeout=5
    )
    return resp.status_code