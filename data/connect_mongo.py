from pymongo.mongo_client import MongoClient
import os

# export MONGO_KEY='<password>' 
mongo_password = os.environ.get('MONGO_KEY')
uri = f"mongodb+srv://qwe9887476:{mongo_password}@cluster0.zflrkw0.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)