import os , environ
from pprint import pprint
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
    URIAction,
)
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
"経歴：エンジニア←社内SE←通信回線営業←通信回線設定業者\n"\
"現在の主な業務：開発,コードレビュー,外注の管理,"\
"依頼,仕様設計,詳細設計,クライアントヒアリング,"\
"エンジニア面接,etc…"\

title_skill = "スキルセット"
skill = "OS：Windows,Mac,linux\n"\
"DB：MySQL\n"\
"言語：PHP,Python,Swift,Kotlin,JS,HTML,CSS"\
"インフラ：AWS(VPC,EC2,Lambda,CloudWatch,Route53,S3,IAM,RDS,Athena,"\
"Glue),Docker,etc…"\
"API：LINE,twilio,Twitter,SendGrid,Gmo,veritrans,\n"\
"UPC,square,smaregi,nec,etc…"\

title_work = "なにができるの？"
work ="EC、モバイルオーダー、予約システムなどの\n"\
"開発が多く外部のAPIの利用も多く知見は深いです。\n"\
"特にAPIの仕様を理解するのが早いです。\n\n"\
"メイン言語はPHP,JSです。\n"\
"その他の言語は軽くバグ修正などで触っています。\n"\
"スタートアップということもあり、幅広い業務を担当しています。\n"\


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

    def set_box_margin(self,contents):
        box=BoxComponent(
          layout='vertical',
          margin="xxl",
          contents=contents,
        )
        return box

    def set_box_horizontal(self,contents):
        box=BoxComponent(
          layout='horizontal',
          contents=contents,
        )
        return box
      
    def set_action(self, label , uri):
      action =  URIAction("action", uri)
      return  action
    
    def set_transation_title(self,text):
        titleComponent = TextComponent(
          text = text,
          weight = "bold",
          color  = "#555555",
          size   = "xl",
          margin = "md",
          wrap   = True,
        )
        return titleComponent

    def detailAction(self,action):
        Component = TextComponent(
          text = "詳細",
          color  = "#111111",
          size   = "sm",
          margin = "md",
          align = "end",
          action = action
        )
        return Component  

    def set_detail_title(self,title):
        Component = TextComponent(
          text = title,
          color  = "#555555",
          size   = "sm",
          flex = 0,
        )
        return Component  


    def transactionSendMessage(self, scanUrl , walletUrl , sendText):
        
        walletAction = self.set_action(walletUrl , walletUrl)
        detail_component = self.detailAction(walletAction)
        detail_title_Component = self.set_detail_title("Wallet")
        wallet_box = self.set_box_horizontal([detail_title_Component,detail_component])
        wallet_box = self.set_box_margin([wallet_box])

        scanAction = self.set_action(scanUrl , scanUrl)
        detail_component = self.detailAction(scanAction)
        detail_title_Component = self.set_detail_title("Scan")
        scan_box = self.set_box_horizontal([detail_title_Component,detail_component])
        scan_box = self.set_box_margin([scan_box])
        separator_component = self.set_separator()
        title_component = self.set_transation_title(sendText)
        box = self.set_box_margin([title_component,separator_component,wallet_box,scan_box])
        response = line_bot_api.reply_message(
            self.event.reply_token,
            FlexSendMessage(
              alt_text=sendText,
              contents=BubbleContainer(
                  direction='ltr',
                  body=box
              )
            )
        )
