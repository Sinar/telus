from pymongo import MongoClient
import json
import os
import datetime


class DocumentProcessor(object):
    def __init__(self, datapath, uri='mongodb://localhost:27017/', db="ocds_hack"):
        self.client = MongoClient(uri)
        self.datapath = datapath
        self.db = self.client[db]

    def read_jsonl(self):
        for item in os.listdir(self.datapath):
            # TODO: Might need a path.join here
            f = open(os.path.join(self.datapath,item))
            for entry in f:
                data = json.loads(entry)
                yield data

    
    # Assume data is well formed
    def store_record(self, collection_name, data):
        print(data)
        collection = self.db[collection_name]
        if "_id" in data:
            del data["_id"]
        collection.update({"id":data["id"]}, data, upsert=True)
        


    # Assume item_id is in ocid. 
    def fetch_record(self, collection_name, item_id):
        collection = self.db[collection_name]
        return collection.find_one({"ocid":item_id})

    # warning this return cursor
    def fetch_records(self, collection_name):
        collection = self.db[collection_name]
        return collection.find()

    def search(self, collection_name, key, value):
        collection = self.db[collection_name]
        return colelction.find({ key: value }) 


