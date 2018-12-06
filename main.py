import time

from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin
from redis import Redis
from wechatpy import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from wechatpy.utils import random_string

# wechatpy
redis_client = Redis.from_url("redis://127.0.0.1:6379/0")
session_interface = RedisStorage(redis_client, prefix="wechatpy")
appid = "wx864c69fe65dd3965"
secret = "61e14f509405ddb041b5c08c552691ee"
client = WeChatClient(
    appid=appid,
    secret=secret,
    session=session_interface
    )


app = Sanic()
CORS(app)
@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/jssdk_config")
async def jssdk_config(request):
    url = request.headers.get("referer")
    ticket = client.jsapi.get_jsapi_ticket()
    timestamp = int(time.time())
    nonce_str = random_string()
    signature = client.jsapi.get_jsapi_signature(nonce_str, ticket, timestamp, url)
    
    return json({
        "appid": appid,
        "timestamp": timestamp,
        "noncestr": nonce_str,
        "signature": signature,
        "url": url
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
