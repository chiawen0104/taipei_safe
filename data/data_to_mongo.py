import pymongo
import json
import os
 
# export MONGO_KEY='<password>' 
mongo_password = os.environ.get('MONGO_KEY')
client = pymongo.MongoClient(f"mongodb+srv://qwe9887476:{mongo_password}@cluster0.zflrkw0.mongodb.net/?retryWrites=true&w=majority")
db = client.taipei
collection = db.case
requesting = []
collection.delete_many({})

with open('./li_data.json', 'r') as f:
    myList = json.load(f)
    # print(len(myList))

result = collection.insert_many(myList)
client.close()