from typing import Dict, Any
from fastapi import FastAPI
from models import Event
from handlers import event_handler

app = FastAPI()


@app.get("/")
async def root():
    """测试环境API
    """
    return {"message": "all right!"}


@app.post("/event")
def event(event: Event):
    """事件上报
    """
    event_handler(event)
    return {}