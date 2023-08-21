# taipei_safe


## Packages
Flask==2.3.2
requests==2.31.0
pymongo==4.4.1
numpy==1.23.1
geopy==2.3.0
dnspython==2.4.0
line-bot-sdk==3.1.0

## Demo
```
python3 demo/main.py
```


## Mongo DB 
Do not use these commands when running demo.

### Connect to the cluster 
```
python -m pip install pymongo==3.6
python3 data/connect_mongo.py
```

### Import json data to the database
```
python3 data/data_to_mongo.py
```
