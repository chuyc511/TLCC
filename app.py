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

spec_group_id = os.getenv('GROUP_ID', '')

owner_user_id = os.getenv('OWNER_USER_ID', '')
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
    user_id = event.source.user_id
    group_id = None

    if hasattr(event.source, 'group_id'):
        group_id = event.source.group_id

    if group_id == spec_group_id or user_id == owner_user_id:

        msg = event.message.text

        line_name = None

        try:
            line_name = lineBotApi.get_profile(user_id).display_name
        except Exception:
            print(f'user_id: {user_id} -> get_profile error')

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
            
            now_datetime = datetime.now()
            now_datetime_str = now_datetime.strftime('%Y-%m-%d')

            team = query_team(now_datetime_str)

            if team.date is not None:
                lineBotApi.reply_message(
                    event.reply_token, 
                    [
                        TextSendMessage(text = '組隊建過了！(｀⌒´メ)'), 
                        TextSendMessage(text = get_team_message(team))
                    ]
                )
            else:
                weekday = now_datetime.isoweekday()

                defult_user_id = None

                if weekday <= 5:
                    defult_user_id = qiang_user_id

                create_team(now_datetime_str, defult_user_id)

                team = query_team(now_datetime_str)

                lineBotApi.reply_message(
                    event.reply_token, 
                    [
                        TextSendMessage(text = '組隊建立成功！(。・`ω´・)'), 
                        TextSendMessage(text = get_team_message(team))
                    ]
                )
        elif msg.startswith('/Team'):
            
            now_datetime = datetime.now()
            now_datetime_str = now_datetime.strftime('%Y-%m-%d')

            team = query_team(now_datetime_str)

            if team.date is not None:
                lineBotApi.reply_message(
                    event.reply_token,
                    TextSendMessage(text = get_team_message(team))
                )
            else:
                lineBotApi.reply_message(
                    event.reply_token,
                    TextSendMessage(text = '還沒建組隊，別急！')
                )
        elif msg.startswith('/+1'):
            
            now_datetime = datetime.now()
            now_datetime_str = now_datetime.strftime('%Y-%m-%d')
            weekday = now_datetime.isoweekday()

            over_time = False

            if weekday <= 5 and now_datetime > datetime.strptime(f'{now_datetime_str} 19:45:00', '%Y-%m-%d %H:%M:%S'):
                over_time = True

            if weekday > 5 and now_datetime > datetime.strptime(f'{now_datetime_str} 13:15:00', '%Y-%m-%d %H:%M:%S'):
                over_time = True

            if over_time:
                lineBotApi.reply_message(
                    event.reply_token, 
                    TextSendMessage(text = '已逾時！')
                )
            else:
                team = query_team(now_datetime_str)

                if team.date is None:

                    defult_user_id = None

                    if weekday <= 5:
                        defult_user_id = qiang_user_id

                    create_team(now_datetime_str, defult_user_id)

                    team = query_team(now_datetime_str)

                    lineBotApi.reply_message(
                        event.reply_token, 
                        TextSendMessage(text = '組隊建立成功！(。・`ω´・)')
                    )

                user_list = query_users()

                if any(record.user_id == user_id for record in user_list):

                    isSuccess = True
                    isRepeat = False

                    tianlong_name = ''

                    for record in user_list:
                        if record.user_id == user_id:
                            tianlong_name = record.tianlong_name
                            break

                    if team.member_a == user_id:
                        isRepeat = True
                        isSuccess = False
                    elif team.member_b == user_id:
                        isRepeat = True
                        isSuccess = False
                    elif team.member_c == user_id:
                        isRepeat = True
                        isSuccess = False
                    elif team.member_d == user_id:
                        isRepeat = True
                        isSuccess = False
                    elif team.member_e == user_id:
                        isRepeat = True
                        isSuccess = False
                    elif team.member_f == user_id:
                        isRepeat = True
                        isSuccess = False
                    else:
                        if team.member_a is None:
                            team.member_a = user_id
                            team.member_a_name = tianlong_name
                            update_team_member_a(now_datetime_str, user_id)
                        elif team.member_b is None:
                            team.member_b = user_id
                            team.member_b_name = tianlong_name
                            update_team_member_b(now_datetime_str, user_id)
                        elif team.member_c is None:
                            team.member_c = user_id
                            team.member_c_name = tianlong_name
                            update_team_member_c(now_datetime_str, user_id)
                        elif team.member_d is None:
                            team.member_d = user_id
                            team.member_d_name = tianlong_name
                            update_team_member_d(now_datetime_str, user_id)
                        elif team.member_e is None:
                            team.member_e = user_id
                            team.member_e_name = tianlong_name
                            update_team_member_e(now_datetime_str, user_id)
                        elif team.member_f is None:
                            team.member_f = user_id
                            team.member_f_name = tianlong_name
                            update_team_member_f(now_datetime_str, user_id)
                        else:
                            isSuccess = False

                    if isSuccess:
                        lineBotApi.reply_message(
                            event.reply_token, 
                            [
                                TextSendMessage(text = '加入成功！'), 
                                TextSendMessage(text = get_team_message(team))
                            ]
                        )
                    elif isRepeat:
                        lineBotApi.reply_message(
                            event.reply_token, 
                            [
                                TextSendMessage(text = '加過了！(｀⌒´メ)'), 
                                TextSendMessage(text = get_team_message(team))
                            ]
                        )
                    else:
                        lineBotApi.reply_message(
                            event.reply_token, 
                            [
                                TextSendMessage(text = '滿人啦！'), 
                                TextSendMessage(text = get_team_message(team))
                            ]
                        )
                else:
                    lineBotApi.reply_message(
                        event.reply_token, 
                        TextSendMessage(text = '你沒註冊！(｀⌒´メ)')
                    )
        elif msg.startswith('/-1'):
            
            now_datetime = datetime.now()
            now_datetime_str = now_datetime.strftime('%Y-%m-%d')
            weekday = now_datetime.isoweekday()

            over_time = False

            if weekday <= 5 and now_datetime > datetime.strptime(f'{now_datetime_str} 19:45:00', '%Y-%m-%d %H:%M:%S'):
                over_time = True

            if weekday > 5 and now_datetime > datetime.strptime(f'{now_datetime_str} 13:15:00', '%Y-%m-%d %H:%M:%S'):
                over_time = True

            if over_time:
                lineBotApi.reply_message(
                    event.reply_token, 
                    TextSendMessage(text = '已逾時！')
                )
            else:
                user_list = query_users()

                if any(record.user_id == user_id for record in user_list):

                    team = query_team(now_datetime_str)

                    if team.date is not None:

                        isSuccess = True
                        
                        if team.member_a == user_id:
                            team.member_a = None
                            team.member_a_name = None
                            update_team_member_a(now_datetime_str, None)
                        elif team.member_b == user_id:
                            team.member_b = None
                            team.member_b_name = None
                            update_team_member_b(now_datetime_str, None)
                        elif team.member_c == user_id:
                            team.member_c = None
                            team.member_c_name = None
                            update_team_member_c(now_datetime_str, None)
                        elif team.member_d == user_id:
                            team.member_d = None
                            team.member_d_name = None
                            update_team_member_d(now_datetime_str, None)
                        elif team.member_e == user_id:
                            team.member_e = None
                            team.member_e_name = None
                            update_team_member_e(now_datetime_str, None)
                        elif team.member_f == user_id:
                            team.member_f = None
                            team.member_f_name = None
                            update_team_member_f(now_datetime_str, None)
                        else:
                            isSuccess = False

                        if isSuccess:
                            lineBotApi.reply_message(
                                event.reply_token, 
                                [
                                    TextSendMessage(text = '退出成功！(｀⌒´メ)'), 
                                    TextSendMessage(text = get_team_message(team))
                                ]
                            )
                        else:
                            lineBotApi.reply_message(
                                event.reply_token, 
                                [
                                    TextSendMessage(text = '又沒加入！(｀⌒´メ)'), 
                                    TextSendMessage(text = get_team_message(team))
                                ]
                            )
                    else:
                        lineBotApi.reply_message(
                            event.reply_token, 
                            TextSendMessage(text = '還沒建組隊，-1？？？')
                        )
                else:
                    lineBotApi.reply_message(
                        event.reply_token, 
                        TextSendMessage(text = '你沒註冊！(｀⌒´メ)')
                    )
        else:
            1
          
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)