## go-cqhttp机器人客户端

基于go-cqhttp的机器人客户端，事件上报采用反向HTTP POST，消息发送采用HTTP API

### 实现功能

- [x] 舔狗日记
- [x] 一言
- [x] 实时天气查询
- [x] 多语言文本翻译
- [x] 文本转二维码
- [x] 网易云音乐+QQ音乐点歌
- [x] 知乎搜索

### 项目依赖

HTTP服务端采用[FastAPI](https://github.com/tiangolo/fastapi)

HTTP请求采用[requests](https://github.com/psf/requests)

实时天气查询采用[天气API](https://tianqiapi.com/)

文本翻译采用[有道智云文本翻译服务](https://ai.youdao.com/product-fanyi-text.s)

### 安装环境

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 启动服务
```bash
uvicorn main:app --reload
```

