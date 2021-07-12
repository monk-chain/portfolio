from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from monk.line_message import LineMessage
import os
import environ
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
import json
from linebot.models import (
    MessageEvent,
    TextMessage,
)
from pprint import pprint
BASE_DIR = environ.Path(__file__) - 2
env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)
YOUR_CHANNEL_SECRET = env("LINE_MESSAGE_SECRET")
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

CONTACT ="問い合わせのご連絡ありがとうございます。\n"\
"大変恐縮でございますが、下記のテンプレートからメールにてご連絡お願いいたします。\n\n"\
"to：monk.developper@gmail.com"\
"会社名（任意）：\n"\
"氏名（任意）：\n"\
"連絡先：\n"\
"問い合わせ項目：\n"\

@csrf_exempt
def webhook(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)


@handler.add(MessageEvent, message=TextMessage)
def webhookMain(event):
    send_text = event.message.text
    print(send_text)
    if send_text == "INFO":
        line_message = LineMessage(event)
        line_message.infoMessage(send_text)   
    elif send_text == "SKILL":
        line_message = LineMessage(event)
        line_message.textMessage(linefeed(env(send_text)))
    elif send_text == "CONTACT":
        line_message = LineMessage(event)
        line_message.textMessage(CONTACT)

@csrf_exempt
def orgdebug(request):
    # print(vars(line_bot_api))
    # print(vars(handler))
    print(linefeed(env("SKILL")))
    html="<h1>Hello World</h1>"
    return HttpResponse(html)

def linefeed(text):
    return text.replace('-', os.linesep)