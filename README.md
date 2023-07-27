# taipei_safe


## Packages
```
pip install Flask
pip install pymongo
pip install dnspython
pip install line-bot-sdk
```


## Demo
```
python3 demo/main.py
```


## Mongo DB 
You don't need to use these commands when running demo.

### Connect to the cluster 
```
python -m pip install pymongo==3.6
python3 data/connect_mongo.py
```

### Import json data to the database
```
python3 data/data_to_mongo.py
```
