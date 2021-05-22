from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class Sex(str, Enum):
    """发送者的性别枚举
    """
    male = "male"
    female = "female"
    unknown = "unknown"


class PostType(str, Enum):
    """事件类型枚举
    """
    message = "message"
    notice = "notice"
    request = "request"
    meta_event = "meta_event"


class MessageType(str, Enum):
    """消息事件中消息的类型
    """
    private = "private"
    group = "group"


class MessageSubType(str, Enum):
    """消息子类型
    """
    # 私聊消息子类型
    friend = "friend"
    group = "group"
    other = "other"
    # 群聊消息子类型
    normal = "normal"
    anonymous = "anonymous"
    notice = "notice"


class Anonymous(BaseModel):
    """匿名用户信息
    """
    id: int
    name: str
    flag: str


class Sender(BaseModel):
    """发送者信息(不保证每个字段都一定存在)
    """
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    card: Optional[str] = None
    sex: Optional[Sex] = None
    age: Optional[int] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None


class Event(BaseModel):
    """事件数据
    """
    # 每个事件都有的字段
    time: datetime
    self_id: int
    post_type: PostType
    # 私聊消息
    message_type: Optional[MessageType] = None
    sub_type: Optional[MessageSubType] = None
    message_id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None
    raw_message: Optional[str] = None
    font: Optional[int] = None
    sender: Optional[Sender] = None
    # 群聊消息
    group_id: Optional[int] = None
    anonymous: Optional[Anonymous] = None


class QuickReply(BaseModel):
    """快速回复信息
    """
    reply: str
    auto_escape: bool
    at_sender: Optional[bool] = None
    delete: Optional[bool] = None
    kick: Optional[bool] = None
    ban: Optional[bool] = None
    ban_duration: Optional[int] = None