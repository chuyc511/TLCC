import os

import json

from user import User

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)

from linebot.models import *

app = Flask(__name__)

userArr = [
    User("U5214b9445dd5fff0c1d821b01fc2e855", "Rio", "Lemon"),
    User("U41370a3e3c73137f6f272e20c1e6b8cc", "小桃", "絕代小桃")
]

# Channel Access Token
lineBotApi = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN', ''))
# Channel Secret
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET', ''))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods = ['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    print(f'event: {str(event)}')
    print(f'type(event): {type(event)}')
    msg = event.message.text
    userId = event.source.userId
    profile = lineBotApi.get_profile(userId)
    print(f'profile: {str(profile)}')
    print(f'type(profile): {type(profile)}')
    lineName = profile.displayName

    if msg.startswith('/RegisterTianLong'):
        tianLongNameArr = msg.split('-', 1)
        tianLongName = ''

        if len(tianLongNameArr) == 2:
            tianLongName = tianLongNameArr[1]
            if any(user.userId == userId for user in userArr):
                for item in userArr:
                    if item.userId == userId:
                        item.lineName = lineName
                        item.tianLongName = tianLongName
                        break
            else:
                userArr.append(User(userId, lineName, tianLongName))
                
        message = TextSendMessage(text = f'Line={lineName}, TianLong={tianLongName}')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/GetCurrentUserInfo'):
        for item in userArr:
            print(f'userId={item.userId}, displayName={item.lineName}, alias={item.tianLongName}')
        
        message = TextSendMessage(text = f'GetCurrentUserInfo')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/+1'):
        message = TextSendMessage(text = 'OK')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/+2'):
        message = TextSendMessage(text = 'OK')
        lineBotApi.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text = msg)
        lineBotApi.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = lineBotApi.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text = f'{name}歡迎加入')
    lineBotApi.reply_message(event.reply_token, message)
            
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
