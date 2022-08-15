from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
from flask_cors import CORS
import json
import os
import pymongo
import base64
# not using yet
import numpy as np
import requests
import io
# from io import BytesIO
from scipy.io.wavfile import read, write
# from flask_pymongo import PyMongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables

DATABASE_URI = os.environ.get("MONGO_URI")
# establish connection with database
client = pymongo.MongoClient(DATABASE_URI)
mongo_db = client.trafficlight  # assign the specific database to mongo_db
# collections available: audiobooks, wakeup

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
    Pooh_book = mongo_db.audiobooks.find_one(
        {"title": "Winnie the Pooh"})  # get all documents (only 1)
    first_chapter = Pooh_book["chapters"][0]
    songCount = mongo_db.audiobooks.count_documents({})
    numberOfChapters = songCount
    return jsonify(numberOfChapters, first_chapter), 200

# goal: play a wake up song
# https://medium.com/analytics-vidhya/extracting-audio-files-from-api-storing-it-on-a-nosql-database-789c12311a48

# {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song}


@app.route("/alarmsong/<name>", methods=["GET"])
def get_wake_up_song(name):
    songObject = mongo_db.wakeup.find_one({'name': name})  # fine song by name
    print(type(songObject['data']))
    # response = songObject['data']

    # response = write(name, np.fromiter(songObject["data"], np.int16))
    decoded = base64.decodebytes(songObject['data'])

    # responseFile = io.BytesIO(decoded)

    # responseFile = io.BytesIO(songObject['data'])
    # next try to put responseFile back into io.B

    # flask.send_file(decoded)
    return send_file(
        io.BytesIO(decoded),
        mimetype=songObject['type'],
        as_attachment=False,
        filename_=songObject['name']), 200

    # response = make_response(decoded)
    # response.headers['Content-Type'] = songObject['fileType']
    # response.headers["Content-Dispostion"] = 'inline'

    # return jsonify(response), 200
    # return send_file(responseFile, mimesongObject['type'] ), 200

    # response = write(name=name, data=songObject['data'])
    # .read(
    #     0, len(songObject['data'])))


# function to check if file to upload is already in the DB:
# def is_song_in_db():
    # pass
    # songCount = mongo_db.wakeup.countDocuments({'name': fileDetails.filename})
    # fileDetails = request.files['song-file']
    # if fileDetails not in songs:
    #     mongo_db.wakeup.insert_one(
    #         {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song})
    #     print("BSON song added to database!!")
    # else:
    #     print('file already in DB. No new file added')

    #  From axios, songData is sent:songData.append('song-file', songFile);
    # https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
@app.route("/alarmsong", methods=["POST"])
def add_wake_up_song():
    if 'song-file' not in request.files:
        print("song not here.")
    else:
        # <FileStorage: 'PAW Patrol.wav' ('audio/wav')>
        print(f"Here is the song-file: {request.files['song-file']}")
        fileDetails = request.files['song-file']
        # print(dir(fileDetails)) 'content_type', 'filename',
        new_song = request.files['song-file'].read()
        print(type(new_song))  # <class 'bytes'>

        songCount = mongo_db.wakeup.count_documents(
            {'name': fileDetails.filename})
        if songCount > 0:
            return 'file already in DB. No new file added'
        elif songCount == 0:
            # {'name': 'PAW Patrol.mp3', 'type': 'audio/mpeg'}
            print({'name': fileDetails.filename, 'type': fileDetails.content_type})
            mongo_db.wakeup.insert_one(
                {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song})
            response = f"{fileDetails.filename} audio file added to database, sent as bson!"
    return jsonify(response), 201


# {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song}
# This routes returns all available songs names in wakeup collection
@app.route("/playmusic", methods=["GET"])
def get_music():
    music = mongo_db.wakeup.find()
    song_list = []
    for song in music:
        song_list.append(song['name'])
    return ({'songList': song_list})

# {"songList": ["PAW Patrol.mp3", "The Lion King - I Just Cant Wait to be King.mp3", "Un bolero de soledad.mp3" ]}


if __name__ == 'main':
    app.run()


# tutorial:
# https://medium.com/analytics-vidhya/deploy-a-web-api-with-python-flask-and-mongodb-on-heroku-in-10-mins-71c4571c505d
