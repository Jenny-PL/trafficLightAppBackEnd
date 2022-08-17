from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
from flask_cors import CORS
import os
import pymongo
import io

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
DATABASE_URI = os.environ.get("MONGO_URI")

# establish connection with database
client = pymongo.MongoClient(DATABASE_URI)
# assign the specific database to mongo_db
mongo_db = client.trafficlight
# collections available: audiobooks, wakeup

app = Flask(__name__)
CORS(app)


@app.route("/")
def test_route():
    return "capstone project!"


# Search for song by name, return audiofile
@app.route("/alarmsong/<name>", methods=["GET"])
def get_wake_up_song(name):
    songObject = mongo_db.wakeup.find_one({'name': name})
    print(type(songObject['data']))

    responseFile = io.BytesIO(songObject['data'])

    return send_file(
        responseFile,
        mimetype=songObject['type'],
        as_attachment=False), 200


# Send uploaded audio file to database:
# {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song}
@app.route("/alarmsong", methods=["POST"])
def add_wake_up_song():
    if 'song-file' not in request.files:
        print("song not here.")
    else:
        print(f"Here is the song-file: {request.files['song-file']}")
        fileDetails = request.files['song-file']
        new_song = request.files['song-file'].read()
        print(type(new_song))  # <class 'bytes'>

        songCount = mongo_db.wakeup.count_documents(
            {'name': fileDetails.filename})
        if songCount > 0:
            return 'file already in DB. No new file added'
        elif songCount == 0:
            print({'name': fileDetails.filename, 'type': fileDetails.content_type})
            # {'name': 'PAW Patrol.mp3', 'type': 'audio/mpeg'}
            mongo_db.wakeup.insert_one(
                {'name': fileDetails.filename, 'type': fileDetails.content_type, 'data': new_song})
            response = f"{fileDetails.filename} audio file added to database, sent as bson!"
    return jsonify(response), 201


# This routes returns all available songs names in wakeup collection
# Example: {"songList": ["PAW Patrol.mp3", "The Lion King - I Just Cant Wait to be King.mp3", "Un bolero de soledad.mp3" ]}
@app.route("/playmusic", methods=["GET"])
def get_music():
    music = mongo_db.wakeup.find()
    song_list = []
    for song in music:
        song_list.append(song['name'])
    return ({'songList': song_list})


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


if __name__ == 'main':
    app.run()
