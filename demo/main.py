# encoding = "utf-8"
from flask import Flask, render_template, request
import requests
import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pymongo
import numpy as np


'''Mongo DB'''
# please set the environment variable before executing the code
# export MONGO_KEY='asdzxc8914' 
mongo_password = os.environ.get('MONGO_KEY')
client = pymongo.MongoClient(f"mongodb+srv://qwe9887476:{mongo_password}@cluster0.zflrkw0.mongodb.net/?retryWrites=true&w=majority")
db = client.taipei.case

# query data in database 
# for x in db.find():
#     print(x)



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



@app.route('/report', methods=['GET', 'POST'])
def report():

    document = None
    if request.method == 'POST':
        li = request.form['li']
        date = request.form['date']
        case_type = request.form['type']

        query = {'li':li}
        if db.count_documents(query) > 0:
            # update one li's data
            db.update_one(query, {'$inc': {case_type: 1, 'total': 1}})

            # compute new median and std of total values
            total_list = []
            for old in db.find():
                total_list.append(old['total'])
            
            new_med = np.median(total_list)
            new_std = np.std(total_list)
            green_score = new_med - new_std
            red_score = new_med + new_std
            
            # update each li's label
            for new in db.find():
                new_label = ''
                if new['total'] > red_score: new_label = 'red'
                elif new['total'] < green_score: new_label = 'green'
                else: new_label = 'yellow'
                if new['label'] != new_label:
                    db.update_one(
                        {'li': new['li']},
                        {'$set': {'label': new_label}}
                    )

            document = db.find_one(query)
            print('Finish db update!')

        else:
            document = ''
            print('No data found!')


    return render_template('report.html', document=document)



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
    app.run(host="0.0.0.0", port=8888, debug=True)