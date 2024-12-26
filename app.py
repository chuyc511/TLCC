import os

from datetime import datetime

from dotenv import load_dotenv

from dao import *
from message import *

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)

from linebot.models import *

app = Flask(__name__)

load_dotenv()

# Channel Access Token
lineBotApi = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', ''))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', ''))

group_id = os.getenv('GROUP_ID', '')

owner_user_id = os.getenv('ADMIN_USER_ID', '')
qiang_user_id = os.getenv('QIANG_USER_ID', '')

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
    user_id = event.source.user_id
    profile = lineBotApi.get_profile(user_id)
    line_name = profile.display_name

    if msg.startswith('/RegisterTianLong'):
        tianlong_name_list = msg.split('-', 1)
        tianlong_name = line_name

        if len(tianlong_name_list) == 2:
            tianlong_name = tianlong_name_list[1]

        user_list = query_users()

        if any(record.user_id == user_id for record in user_list):
            update_user(user_id, line_name, tianlong_name)
        else:
            create_user(user_id, line_name, tianlong_name)
        
        message = TextSendMessage(text = f'Line:{line_name}\nTianLong:{tianlong_name}')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/NewTeam') and user_id == owner_user_id:

        today_str = datetime.today().strftime('%Y-%m-%d')

        team = query_team(today_str)

        if team.date is not None:
            lineBotApi.reply_message(
                event.reply_token, 
                [
                    TextSendMessage(text = '已建立組隊！'), 
                    TextSendMessage(text = get_team_message(team))
                ]
            )
        else:
            create_team(today_str, qiang_user_id)

            team = query_team(today_str)

            lineBotApi.reply_message(
                event.reply_token, 
                [
                    TextSendMessage(text = '組隊建立成功！'), 
                    TextSendMessage(text = get_team_message(team))
                ]
            )
    elif msg.startswith('/+1'):


        message = TextSendMessage(text = '+1 OK')
        lineBotApi.reply_message(event.reply_token, message)
    elif msg.startswith('/-1'):


        message = TextSendMessage(text = '-1 OK')
        lineBotApi.reply_message(event.reply_token, message)
    else:
        print(f'userId:{user_id}')
        print(f'lineName:{line_name}')
        print(f'message:{msg}')
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
    port = int(os.getenv('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
