# taipei_safe
【金獎】資料創新應用競賽—臺北市科技普惠市政創新應用組
「北市智慧安全小幫手：安心地圖2.0與治安回歸分析」

## Packages
```
Flask==2.3.2  
requests==2.31.0  
pymongo==4.4.1  
numpy==1.23.1  
geopy==2.3.0  
dnspython==2.4.0  
line-bot-sdk==3.1.0
```

## Run Demo
```
python3 demo/main.py
```

## Deploy to GCP
```
bash deploy/deploy_remote.sh
```

## Mongo DB 
Do not use these commands during Demo.

### Connect to the database 
```
python -m pip install pymongo==3.6
python3 data/connect_mongo.py
```

### Import json data to the database
```
python3 data/data_to_mongo.py
```
