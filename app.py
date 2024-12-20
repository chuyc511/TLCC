import os
import json

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)

from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN', ''))
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
    # groupId = event.source.groupId
    # userId = event.source.userId
    # profile = line_bot_api.get_group_member_profile(groupId, userId)
    # name = profile.display_name


    if 'info' in msg:
        # displayName = msg.
        # message = TextSendMessage(text = f'uid={name}, gid={groupId}, userId={userId}, name={name}, displayName={displayName}')
        jsonstr = json.dumps(event.__dict__)
        message = TextSendMessage(text = f'info={jsonstr}')
        line_bot_api.reply_message(event.reply_token, message)
    elif '+1' in msg:
        message = TextSendMessage(text = 'OK')
        line_bot_api.reply_message(event.reply_token, message)
    elif '+2' in msg:
        message = TextSendMessage(text = 'OK')
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text = msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text = f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
            
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
