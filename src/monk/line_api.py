from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from monk.line_message import LineMessage
from monk.line_blockchain import LineBlockChain
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
line_block_chain = LineBlockChain()
CONTACT ="問い合わせのご連絡ありがとうございます。\n"\
"大変恐縮でございますが、下記のテンプレートからメールにてご連絡お願いいたします。\n\n"\
"↓↓↓宛先はこちら↓↓↓\nmonk.developper@gmail.com\n\n"\
"\n"\
"会社名（任意）：\n"\
"氏名（任意）：\n"\
"連絡先：\n"\
"問い合わせ項目：\n"\
    
STUDY="ブロックチェーンの学習を中心に学んでいます。\n"\
"枠が一つ空いたので、この項目は少し手抜きになってます。\n"\
"(・ω≦) ﾃﾍﾍﾟﾛ"\

SCANHOST   = "https://explorer.blockchain.line.me/cashew/transaction/"
NFTWALLETHOST = "https://explorer.blockchain.line.me/cashew/address/"+env("UserAWallet")
TOKENWALLETHOST = "https://explorer.blockchain.line.me/cashew/address/"+env("UserBWallet")
SENDMESSAGE="を送信しました。"

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
    line_message = LineMessage(event)
    
    if send_text == "INFO":
        line_message.infoMessage(send_text)   

    elif send_text == "NFT":
        response = line_block_chain.POST_v1_item_tokens_contractId_non_fungibles_tokenType_mint()
        pprint(response)
        hash = response['responseData']['txHash']
        scanUrl = SCANHOST+hash
        sendText = send_text + SENDMESSAGE
        line_message.transactionSendMessage(scanUrl , NFTWALLETHOST,sendText)
    
    elif send_text == "TOKEN":
        response =line_block_chain.POST_v1_wallets_walletAddress_service_tokens_contractId_transfer()
        pprint(response)
        hash = response['responseData']['txHash']
        scanUrl = SCANHOST+hash
        sendText = send_text + SENDMESSAGE
        line_message.transactionSendMessage(scanUrl , TOKENWALLETHOST,sendText)
    
    elif send_text == "STUDY":
        line_message.textMessage(STUDY)

    elif send_text == "CONTACT":
        line_message.textMessage(CONTACT)

@csrf_exempt
def orgdebug(request):
    html="<h1>Hello World</h1>"
    return HttpResponse(html)

def linefeed(text):
    return text.replace('-', os.linesep)