import os
import dotenv
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextSendMessage, TextMessage
from linebot.exceptions import InvalidSignatureError

dotenv.load_dotenv()
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')

app = FastAPI()
logger = logging.getLogger('uvicorn')

linebot = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    logger.info(body.decode())
    try:
        handler.handle(body.decode(), request.headers['x-line-signature'])
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail='InvalidSignatureError')
        
    return 'ok'


@handler.add(MessageEvent, TextMessage)
def handle_message(event):
    res_message = TextSendMessage(event.message.text)
    linebot.reply_message(event.reply_token, res_message)
