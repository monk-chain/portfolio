from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.http import HttpResponse
import environ
import logging
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
import json
from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
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

title_info = "どんなひと"
info = "役職：リードエンジニア・開発責任者\n"\
"経歴：社内SE,通信回線営業,通信回線設定業者\n"\
"現在の主な業務：EC系の開発,コードレビュー,外注の管理,"\
"依頼,仕様設計,詳細設計,クライアントヒアリング"\
"エンジニア面接,etc…"\

title_skill = "スキルセット"
skill = "OS：Windows,Mac,linux\n"\
"DB：MySQL\n"\
"言語：PHP,Swift,Kotlin,JS,HTML,CSS"\
"インフラ：AWS(VPC,EC2,Lambda,CloudWatch,Route53,S3,IAM,RDS,Athena,"\
"Glue),Docker,etc…"\
"API：LINE,twilio,SendGrid,Gmo,veritrans,UPC,"\
"square,smaregi,nec,etc…"\

title_work = "なにができるの？"
work ="EC系、モバイルオーダー系、予約システムなどの開発が多く\n"\
"外部のAPIの利用も多く知見は深いです。"\
"特にAPIの仕様を理解するのが早いです。"\
"AWSのCLIをできるだけ利用するようにして、知見を深めてます。"\
"スタートアップということもあり、幅広い業務を担当しています。"\


class LineMessage():
    
    def __init__(self,event, ):
        self.event = event

    def textMessage(self , text):
        pprint((self.event))
        line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(text)
        )

            
    def infoMessage(self,text):
        pprint((self.event))

        box = self.set_info()
        response = line_bot_api.reply_message(
            self.event.reply_token,
            FlexSendMessage(
              alt_text='info',
              contents=BubbleContainer(
                  direction='ltr',
                  body=box
              )
            )
        )
        pprint(vars(response))

    def set_info(self):
      title_info_component = self.set_title(title_info)
      info_component = self.set_main(info)
      title_skill_component = self.set_title(title_skill)
      skill_component = self.set_main(skill)
      title_work_component = self.set_title(title_work)
      work_component = self.set_main(work)
      separator_component = self.set_separator()
      contents = [
        title_info_component ,
        info_component,
        separator_component,
        title_skill_component,
        skill_component,
        separator_component,
        title_work_component,
        work_component,
      ]
      box_component = self.set_box(contents)
      return box_component

    

    def set_separator(self):
        separator = SeparatorComponent(
          margin = "xxl"
        )
        return separator
    
    def set_title(self,text):
        titleComponent = TextComponent(
          text = text,
          weight = "bold",
          color  = "#DDDDDD",
          size   = "xs",
          margin = "lg",
          wrap   = True,
        )
        return titleComponent


    def set_main(self,text):
        mainComponent = TextComponent(
          text   = text,
          type   = "text",
          weight = "bold",
          size   = "xs",
          margin = "md",
          wrap   = True,
        )
        return mainComponent

    def set_box(self,contents):
        box=BoxComponent(
          layout='vertical',
          contents=contents,
        )
        return box


            
