from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

myclient = pymongo.MongoClient(MONGO_URI)

db = myclient['pythonblog']




