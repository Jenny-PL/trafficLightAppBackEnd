from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS

import json
import os
import pymongo
# from flask_pymongo import PyMongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables

DATABASE_URI = os.environ.get("DB_URI")
# establish connection with database
client = pymongo.MongoClient(DATABASE_URI)
mongo_db = client.trafficlight  # assign the specific database to mongo_db

# collections available: audiobooks, playmusic, wakeup

app = Flask(__name__)
CORS(app)


@app.route("/")
def test_route():
    return "capstone project!"


@app.route("/audiobook", methods=["POST"])
def add_audio():
    pass


@app.route("/audiobook", methods=["GET"])
def get_audiobook_chapter():
    # get one chapter from book to play; play in subsequent order
    # for now, just set up to get first chapter:
    # Pooh_book = mongo_db.audiobooks.find_one({"title": "Winnie the Pooh"})

    Pooh_book = mongo_db.audiobooks.find_one(
        {"title": "Winnie the Pooh"})  # get all documents (only 1)
    first_chapter = Pooh_book["chapters"][0]
    return jsonify(first_chapter), 200

# goal: play a wake up song


@app.route("/alarmsong", methods=["GET"])
def get_wake_up_song():
    song = mongo_db.wakeup.find()
    return jsonify(song), 200


# Example POST:
# @app.route("/cocktails/", methods=["POST"])
# def new_cocktail():
#     raw_cocktail = request.get_json()
#     raw_cocktail["date_added"] = datetime.utcnow()

#     cocktail = Cocktail(**raw_cocktail)
#     insert_result = recipes.insert_one(cocktail.to_bson())
#     cocktail.id = PydanticObjectId(str(insert_result.inserted_id))
#     print(cocktail)

#     return cocktail.to_json()

@app.route("/alarmsong", methods=["POST"])
def add_wake_up_song(uploaded_filepath):
    # uploaded_song = request.get_json()
    # new_song = modified uploaded_song?
    # make a song Model?
    new_song = {'uploaded_filepath': uploaded_filepath}
    mongo_db.wakeup.insertOne(new_song)
    return jsonify(new_song), 201
    # dp we still use db.session.add and commit with mongodb??  Think not.
    # mongo_db.wakeup.session.insertOne(new_song)
    # mongo_db.wakeup.session.commit()

# goal: play kids music


@app.route("/playmusic", methods=["GET"])
def get_music():
    music = mongo_db.collection.find()
    return jsonify(music), 200


if __name__ == 'main':
    app.run()

# @app.route("/add_many")
# def add_many():
#     db.todos.insert_many([
#         {'_id': 1, 'title': "todo title one ", 'body': "todo body one "},
#         {'_id': 2, 'title': "todo title two", 'body': "todo body two"},
#         {'_id': 3, 'title': "todo title three", 'body': "todo body three"},
#         {'_id': 4, 'title': "todo title four", 'body': "todo body four"},
#         {'_id': 5, 'title': "todo title five", 'body': "todo body five"},
#         {'_id': 1, 'title': "todo title six", 'body': "todo body six"},
#         ])
#     return flask.jsonify(message="success")

# tutorial:
# https://medium.com/analytics-vidhya/deploy-a-web-api-with-python-flask-and-mongodb-on-heroku-in-10-mins-71c4571c505d
