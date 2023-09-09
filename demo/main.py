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
from geopy.geocoders import Nominatim

'''Mongo DB'''
# please set the environment variable before executing the code
# export MONGO_KEY='asdzxc8914' 
# mongo_password = os.environ.get('MONGO_KEY')
mongo_password = os.environ.get('MONGO_KEY', 'asdzxc8914')
client = pymongo.MongoClient(f"mongodb+srv://qwe9887476:{mongo_password}@cluster0.zflrkw0.mongodb.net/?retryWrites=true&w=majority")
db = client.taipei.case

# query data in database 
# for x in db.find():
#     print(x)



'''Flask'''
app = Flask(__name__)
# default password
password = '1234'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/analysis')
def analysis():
    imagePath = './static/images/regression'
    return render_template('analysis.html', imagePath=imagePath)



@app.route('/report', methods=['GET', 'POST'])
def report():

    sign, render_li, render_label = None, None, None

    if request.method == 'POST':
        li = request.form['li']
        input_password = request.form['password']
        case_type = request.form['type']

        if input_password != password:
            sign = 'wrong'
            return render_template('report.html', sign=sign, li=render_li, label=render_label)

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
            yellow_score = new_med + new_std
            red_score = new_med + 2*new_std
            
            # update each li's label
            for new in db.find():
                new_label = ''
                if new['total'] >= red_score: new_label = 'red'
                elif new['total'] >= yellow_score: new_label = 'yellow'
                else: new_label = 'green'
                if new['label'] != new_label:
                    db.update_one(
                        {'li': new['li']},
                        {'$set': {'label': new_label}}
                    )

            document = db.find_one(query)
            print('Finish db update!')

            sign = 'yes'
            render_li = li
            if document['label'] == 'red': render_label = '紅燈'
            elif document['label'] == 'yellow': render_label = '黃燈'
            else: render_label = '綠燈'

        else:
            sign = 'no'
            print('No data found!')
        
    return render_template('report.html', sign=sign, li=render_li, label=render_label)


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
        ###### 使用者傳送地址訊息
        elif type == 'location':
            lng = json_data['events'][0]['message']['longitude']
            lat = json_data['events'][0]['message']['latitude'] 
            lat_lng = f"{lat}, {lng}"
            print(lat_lng)
            geolocator = Nominatim(user_agent="geoexercise")
            location = geolocator.reverse(lat_lng)
            full_addr_list = location.address.split(",")
            for i in full_addr_list:
                if "里" in i: village = i.strip()
                else: "請再輸入更精確的地址哦~"
            print(str(village))

            for i in db.find():
                if i['li'] == village:
                    if i['label'] == 'green': color = "綠燈 🟢🟢🟢"
                    elif i['label'] == 'yellow': color = "黃燈 🟡🟡🟡"
                    else: color = "紅燈 🔴🔴🔴" 
                    reply = f"以下為 ▶ {i['li']} ◀ 治安資訊:\n🚩強盜: {i['burglary']} 件\n🚩搶劫: {i['robbery']} 件\n🚩自行車竊盜: {i['bike']} 件\n🚩機車竊盜: {i['motocycle']} 件\n🚩汽車竊盜: {i['car']} 件\n🚩住宅竊盜: {i['home']} 件\n🚩總案件數: {i['total']} 件\n\n🚦治安紅綠燈: {color}"
                    break
                else: reply = "查無資料OAO"
        else:
            reply = '我目前還不太懂QAQ'

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