from flask import Flask
from dotenv import load_dotenv
import json
import os
import pymongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables


DATABASE_URI = os.environ.get("DB_URI")

# establish connection with database
client = pymongo.MongoClient(DATABASE_URI)
mongo_db = client.db  # assign database to mongo_db

# mongo_db.launches.drop() # clear the collection

with open('static/data/launches.json') as file:  # opening the json file
    file_data = json.load(file)

if isinstance(file_data, list):
    mongo_db.launches.insert_many(file_data)  # if data is a list
else:
    mongo_db.launches.insert_one(file_data)  # if data is a document object
