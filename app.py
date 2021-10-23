
import os
import datetime
import psycopg2

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction

from custom_models import utils, PhoebeFlex,PhoebeTalks

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):

    #get_message = event.message.text
    # Send To Line
    #reply = TextSendMessage(text= "你說的是不是："+ f"{get_message}")
    #line_bot_api.reply_message(event.reply_token, reply)

    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        reply = False

        # 將資料存入表格中 
        if not reply:
            reply = PhoebeTalks.insert_record(event)
        
        # 發送 FlexMessage
        if not reply:
            reply = PhoebeFlex.img_search_flex(event)
        
        # 幫忙上網找圖
        if not reply:
            reply = PhoebeTalks.img_search(event)
        
        # 裝飾過的回音機器人
        if not reply:
            reply = PhoebeTalks.pretty_echo(event)
    

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #get_message = event.message.text
    # Send To Line
    #reply = TextSendMessage(text= "你說的是不是："+ f"{get_message}")
    #line_bot_api.reply_message(event.reply_token, reply)

    if '草泥馬訓練紀錄' in event.message.text:
        
        try:
            record_list = prepare_record(event.message.text)
            reply = line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
                
        except:

            record_list = prepare_record(event.message.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )
'''

'''
def prepare_record(text):
    text_list = text.split('\n')
    
    month = text_list[0].split(' ')[0].split('/')[0]
    day = text_list[0].split(' ')[0].split('/')[1]
    d = datetime.date(datetime.date.today().year, int(month), int(day))
   
    record_list = []
    
    time_format = '%H:%M'
    
    for i in text_list[1:]:
        temp_list = i.split(' ')
        
        temp_name = temp_list[0]
        temp_training = temp_list[1]
        
        temp_start = datetime.datetime.strptime(temp_list[2].split('-')[0], time_format)
        temp_end = datetime.datetime.strptime(temp_list[2].split('-')[1], time_format)
        temp_duration = temp_end - temp_start
        
        record = (temp_name, temp_training, temp_duration, d)
        record_list.append(record)
        
    return record_list

def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = conn.cursor()

    table_columns = '(alpaca_name, training, duration, date)'
    postgres_insert_query = f"""INSERT INTO alpaca_training {table_columns} VALUES (%s,%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ {cursor.rowcount} 筆資料成功匯入 alpaca_training 表單！"
    print(message)

    cursor.close()
    conn.close()
    
    return message
'''

if __name__ == "__main__":
    app.run()