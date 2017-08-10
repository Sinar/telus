#!/usr/bin/python

from flask import Flask
import json
import pymongo
from bson import Binary, Code
from bson import json_util

app = Flask(__name__)

def json_data1():
    data1_file = open('data/test5a.json','r')
    data1 = json.load(data1_file)
    return data1

def json_data2():
    data2_file = open('data/test5b.json','r')
    data2 = json.load(data2_file)
    return data2

def json_data3():
    data3_file = open('data/test5c.json','r')
    data3 = json.load(data3_file)
    return data3

def mongo_setup(json_list):
    try:
        client = pymongo.MongoClient()
        database = client.test
        collection = database.persons
        print('Create collection was successful')
        collection.drop() # empty collection before insert new data
        collection.insert_many(json_list) # insert collection many at once
        print('Insert JSON data was successful')
    except Exception as e:
        print('Exception: {0}'.format(e))
    finally:
        print('Setup has completed')
    return 0

def mongo_dump():
    try:
        client = pymongo.MongoClient()
        database = client.test
        print('Find collection from MongoDB BSON')
        collection = database.persons.find()
        print('Print data from MongoDB BSON')
        # need to convert cursor object -> JSON string -> JSON literal
        print(collection) # <pymongo.cursor.Cursor object at ...>
        data_list = [] # use an empty list to hold multiple dict
        for item in collection:
            print(item) # {u'_id': ObjectId...}
            parse = json.dumps(item, default=json_util.default)
            print(type(parse)) # <type 'str'>
            print(parse) # {u'_id': "$oid"...}
            parse = json.loads(parse)
            print(type(parse)) # <type 'dict'>
            print(parse)
            data_list.append(parse)
        print('Preview list of dictionaries')
        print(type(data_list))
        print(data_list)
        print('Put the dictionaries into single dictionary...')
        data = {} # start with an empty dict
        data = dict(i for d in data_list for i in d.items())
        print('Preview JSON literal:')
        print(type(data)) # <type 'dict'>
        print(data) # visible u'' strings in terminal emulator only
    except Exception as e:
        print('Exception: {0}'.format(e))
    finally:
        print('Dump has completed')
    return data # return as valid JSON literal

@app.route('/')
@app.route('/home')
def main():
    json_list = [json_data1(), json_data2(), json_data3()] # list JSON data
    print('Input JSON data:')
    source = dict(i for d in json_list for i in d.items()) # add many items
    source_pretty = json.dumps(source, indent=4, sort_keys=True)
    print(source_pretty) # preview input JSON data
    print('Save JSON data to MongoDB BSON...')
    mongo_setup(json_list) # create record and save JSON data
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
