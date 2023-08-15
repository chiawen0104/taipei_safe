# taipei_safe


## Package
```
pip install Flask
pip install pymongo
pip install dnspython
pip install line-bot-sdk
pip install geopy
```


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
