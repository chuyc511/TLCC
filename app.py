import os

from user import User

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)

from linebot.models import *

app = Flask(__name__)

groupId = 'Cd58649e677c5804baffef57b2e345c2b'

userArr = [
    User('U5214b9445dd5fff0c1d821b01fc2e855', 'Rio', '青檸雨上'),
    User('U41370a3e3c73137f6f272e20c1e6b8cc', '阿仙', '絕代小桃'),
    User('U9d221779ff70200dee66bff33031ef2a', '。', '今生緣'),
    User('Uc5591b183ab8278605f37a91c7d3bc1b', '穎璁', '擎宵'),
    User('U86a102f472f6b2725a9c20dc7325f236', '依依老師💜', '尹絮'),
    User('Ud6b102dc9ae832fda916e02678e134f2', 'wind', '凪')
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
    msg = event.message.text
    userId = event.source.user_id
    profile = lineBotApi.get_profile(userId)
    lineName = profile.display_name

    if msg.startswith('/RegisterTianLong'):
        tianLongNameArr = msg.split('-', 1)
        tianLongName = lineName

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
                
        message = TextSendMessage(text = f'Line:{lineName}\nTianLong:{tianLongName}')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/GetCurrentUserInfo') and userId == 'U5214b9445dd5fff0c1d821b01fc2e855':
        tmpResult = ''

        for item in userArr:
            tmpResult += f"User('{item.userId}', '{item.lineName}', '{item.tianLongName}'),\n"
        
        message = TextSendMessage(text = tmpResult)
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/+1'):
        message = TextSendMessage(text = '+1 OK')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/-1'):
        message = TextSendMessage(text = '-1 OK')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/+2'):
        message = TextSendMessage(text = '+2 OK')
        lineBotApi.reply_message(event.reply_token, message)
    else:
        print('handle_message continue...')
        # message = TextSendMessage(text = msg)
        # lineBotApi.reply_message(event.reply_token, message)

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
