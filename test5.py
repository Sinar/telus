#!/usr/bin/python

from flask import Flask
import json
import pymongo
from bson import Binary, Code
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

def json_data():
    data = { "result": [
             { "id": 1,
               "person": { "name": "John Doe", "gender": "Male"},
               "organization": { "name": "Volunteer Team" },
               "post": { "role": "Participant" }
             },
             { "id": 2,
               "person": { "name": "Mary Jane", "gender": "Female"},
               "organization": { "name": "Freelance Group" },
               "post": { "role": "Junior member" }
             },
             { "id": 3,
               "person": { "name": "Thomas Edison", "gender": "Male"},
               "organization": { "name": "Inventor Group" },
               "post": { "role": "Founder" }
             }
              ] }
    return data

def mongo_setup():
    client = pymongo.MongoClient()
    database = client.test
    collection = database.persons
    print('Create collection was successful')
    collection.drop() # empty collection before insert new data
    collection.insert_one(json_data()) # in-built data has one dict only 
    print('Save JSON data has completed')
    return 0

def mongo_dump():
    client = pymongo.MongoClient()
    database = client.test
    collection = database.persons.find()
    print('Find collection was successful')
    # print and convert cursor object to JSON string
    print('Print data from MongoDB BSON')
    print(collection) # <pymongo.cursor.Cursor object at ...>
    data = {} # use an empty dict, unlike { "result": [] } in test4.py
    for item in collection:
        print(item) # {u'_id': ObjectId...}
        data = json.dumps(item, default=json_util.default)
    # preview JSON string output
    print('Preview JSON string:')
    print(type(data)) # <type 'str'>
    print(data)
    # parse into json.loads() to get 'dict' output
    print('Preview JSON literal:')
    data = json.loads(data)
    print(type(data)) # <type 'dict'>
    print(data) # visible u'' strings in Terminal only
    return data # return as valid JSON literal

@app.route('/')
@app.route('/home')
def main():
    print('Input JSON data:')
    source = json_data()
    source_pretty = json.dumps(source, indent=4, sort_keys=True)
    print(source_pretty) # preview input JSON data
    print('Save JSON data to MongoDB BSON...')
    mongo_setup() # create record and save JSON data
    print('Read JSON data from MongoDB BSON...')
    result = mongo_dump() # dump from record to JSON data again
    print('Output JSON data:')
    result_pretty = json.dumps(result, indent=4, sort_keys=True)
    print(result_pretty) # output JSON data should appear similar to input
    result = app.response_class(
                response = json.dumps(result),
                status = 200,
                mimetype = 'application/json')
    print('Output response:')
    print(result) # only response status will be printed here
    return result # return JSON data as object, visible in web browser

if __name__ == '__main__':
    app.run()
