#!/usr/bin/python
"""
This is a module for dealing with MongoDB via PyMongo.

Use this module to manage databases and collections in MongoDB using
the Python driver, PyMongo. The API operation commands have slight
differences between `mongo` shell and `pymongo` in Python scripts.

MongoDB manual (https://docs.mongodb.com/manual/) has notable links
to Getting Started Guide. For writing codes in Python scripts, look
into "Python Edition" instead of "mongo Shell Edition".

For full reference, see MongoDB Ecosystem - Python MongoDB drivers
(https://docs.mongodb.com/ecosystem/drivers/python/) that provides
links to API documentation and other resources.

This module was written with API operation commands that are valid
for PyMongo 3.0 and newer. Avoid deprecated API mentioned by docs.
"""

from __future__ import print_function

import sys
import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util

import lib.query

def test_conn():
    """Test connection to MongoDB server."""
    try:
        print('Using PyMongo {}'.format(pymongo.version))
        client = pymongo.MongoClient(
                    connectTimeoutMS=2000,
                    serverSelectionTimeoutMS=3000)
        client.admin.command("ismaster")
    except pymongo.errors.ConnectionFailure:
        print('Refused connection, check if server is running')
        sys.exit(1)
    else:
        print('Connected to server')

def use_conn():
    """Return client for a MongoDB instance."""
    client = pymongo.MongoClient()
    return client

def set_database(dbname):
    """Return database with specified name on MongoDB."""
    client = use_conn()
    database = client[dbname]
    print('Created database: {}'.format(database.name))
    return database

def set_collection(dbname, ccname):
    """Return collection with specified name on MongoDB."""
    client = use_conn()
    collection = client[dbname][ccname]
    print('Created collection: {}'.format(collection.name))
    return collection

def add_test(ccobject, olist):
    """Test add objects from list into specified collection."""
    if ccobject.count == 0:
        pass
    else:
        print('Collection was not empty, drop first')
        ccobject.drop()
    tcount = 0
    for sobject in olist:
        tcount = tcount + 1
        jobject = json.loads(sobject)
        result = ccobject.insert_one(jobject)
        mobjectid = result.inserted_id
        if tcount == 1:
            fmoid = mobjectid
        else:
            lmoid = mobjectid
        #print('Inserted object {0}: {1}'.format(tcount, mobjectid))
    return fmoid, lmoid

def store_awards(fpath):
    """Store awards from JSONL into MongoDB."""
    print('Prepare to store awards')
    collection = set_collection('telus', 'example')
    listed2, counted2 = lib.query.list_objects(fpath)
    print('Preview counted objects: {}'.format(counted2))
    print('Preview first object: {}'.format(listed2[0]))
    fmoid, _ = add_test(collection, listed2)
    print('Inserted objects: {}'.format(collection.count()))
    rdict_fmoid = collection.find_one({'_id':ObjectId(fmoid)})
    jdict_fmoid = json.dumps(rdict_fmoid, default=json_util.default)
    print('Inserted first object: {}'.format(jdict_fmoid))
