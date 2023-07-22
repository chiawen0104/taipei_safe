# encoding = "utf-8"
from flask import Flask, render_template, request
import requests
import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pymongo


'''Mongo DB'''
# export MONGO_KEY='<password>' 
mongo_password = os.environ.get('MONGO_KEY')
client = pymongo.MongoClient(f"mongodb+srv://qwe9887476:{mongo_password}@cluster0.zflrkw0.mongodb.net/?retryWrites=true&w=majority")
db = client.taipei.case
# for x in db.find():
#     print(x['li'])



'''Flask'''
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/report')
def report():
    return render_template('report.html')


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                   
    try:
        json_data = json.loads(body)                        
        access_token = '你的 line token' ### 輸入自己的 line token
        secret = '你的 line secret' ### 輸入自己的 line secret
        line_bot_api = LineBotApi(access_token)              
        handler = WebhookHandler(secret)                     
        signature = request.headers['X-Line-Signature']      
        handler.handle(body, signature)                      
        tk = json_data['events'][0]['replyToken']           
        type = json_data['events'][0]['message']['type']     
        print(json_data) 

        if type =='text':
            msg = json_data['events'][0]['message']['text']  
            print(msg)                                      
            reply = msg
        ### 使用者傳送地址訊息，回傳訊息中的地址
        elif type == 'location':
            address = json_data['events'][0]['message']['address'].replace('台','臺')
            reply = address
        ###
        else:
            reply = '我目前還看不懂QAQ'

        print(reply)
        line_bot_api.reply_message(tk, TextSendMessage(reply)) #回傳訊息
    except:
        print(body)                                         
    
    return 'OK'                                              


# LINE 回傳訊息函式
def reply_message(msg, rk, token):
    headers = {'Authorization':f'Bearer {token}','Content-Type':'application/json'}
    body = {
    'replyToken':rk,
    'messages':[{
            "type": "text",
            "text": msg
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/reply', headers=headers, data=json.dumps(body).encode('utf-8'))
    print(req.text)


if __name__ == '__main__':
    app.run()