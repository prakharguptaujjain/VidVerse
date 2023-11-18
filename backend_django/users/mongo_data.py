"""
This file stores the data from the json files into the MongoDB database.
Enter correct path of the dataset folder in line 54.
"""

import os
import json
from pymongo import MongoClient

mongodb = "mongodb://localhost:27017/"
database = "VidVerse"
collection = "videos"

client = MongoClient(mongodb)
db = client[database]
col = db[collection]

path = './test/'
files = os.listdir(path)

for file in files:
    path1 = path + file
    data = json.load(open(path1))
    col.insert_one(data)

client.close()