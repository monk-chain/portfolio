from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.http import HttpResponse
import environ
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
import json
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import os
from pprint import pprint
BASE_DIR = environ.Path(__file__) - 2
env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

YOUR_CHANNEL_ACCESS_TOKEN = env("LINE_MESSAGE_TOKEN")
YOUR_CHANNEL_SECRET = env("LINE_MESSAGE_SECRET")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@csrf_exempt
def webhook(request):
    print(request)
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)


@handler.add(MessageEvent, message=TextMessage)
def webhookMain(event):
    if (event.message.text == "skill"):
        pprint((event.message.text))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(linefeed(env("SKILL")))
        )

@csrf_exempt
def orgdebug(request):
    # print(vars(line_bot_api))
    # print(vars(handler))
    print(linefeed(env("SKILL")))
    html="<h1>Hello World</h1>"
    return HttpResponse(html)

def linefeed(text):
    return text.replace('-', os.linesep)