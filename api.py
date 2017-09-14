from flask import Flask
from flask import jsonify
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/<entity>/")
def list_entity(entity):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]

    data = []
    for i in collection.find():
        temp = i
        del temp["_id"]
        data.append(i)
     
    return jsonify({ 'results': data })

@app.route("/<entity>/<id>")
def get_entity(entity, id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]

    result = collection.find_one({"id":id})
    del result["_id"]

    return jsonify({ 'result': result })



