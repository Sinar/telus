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

import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util

def test_conn(host, port):
    """Test connection to MongoDB server."""
    try:
        client = pymongo.MongoClient(
                    host,
                    port,
                    connectTimeoutMS=2000,
                    serverSelectionTimeoutMS=3000)
        client.admin.command("ismaster")
    except pymongo.errors.ConnectionFailure:
        print('Failed to connect')
        raise RuntimeError('Server not available', host, port)
    else:
        print('Connected to server')
        return client

def get_conn(host, port):
    """Return versions of MongoDB and PyMongo when available."""
    client = test_conn(host, port)
    server_version = client.server_info()['version']
    driver_version = pymongo.version
    print('Using MongoDB {0} with PyMongo {1}'.format(
            server_version, driver_version))
    return server_version, driver_version

def use_conn(host, port):
    """Return client for a MongoDB instance."""
    client = test_conn(host, port)
    return client

def set_database(client, dbname):
    """Return database with specified name on MongoDB."""
    database = client[dbname]
    print('Setup database: {}'.format(database.name))
    return database

def set_collection(client, dbname, ccname):
    """Return collection with specified name on MongoDB."""
    collection = client[dbname][ccname]
    print('Setup collection: {}'.format(collection.name))
    return collection

def use_setup(client, dbname, ccname):
    """Return database and collection that were setup on MongoDB."""
    database = set_database(client, dbname)
    collection = set_collection(client, dbname, ccname)
    return database, collection

def add_test(collection, olist):
    """Test add objects from list into specified collection."""
    if collection.count() == 0:
        pass
    else:
        print('Collection was not empty, drop first')
        collection.drop()
    tcount = 0
    for sobject in olist:
        tcount = tcount + 1
        jobject = json.loads(sobject)
        result = collection.insert_one(jobject)
        mobjectid = result.inserted_id
        if tcount == 1:
            fmoid = mobjectid
        else:
            lmoid = mobjectid
        #print('Inserted object {0}: {1}'.format(tcount, mobjectid))
    return fmoid, lmoid

def list_objects(fpath):
    """Return list, count of objects from specified file."""
    slist = []
    lines = 0
    for sobject in open(fpath, 'r'):
        lines = lines + 1
        slist.append(sobject)
    return slist, lines

def store_awards(client, fpath):
    """Store awards from JSONL into MongoDB."""
    print('Prepare to store awards')
    listed2, counted2 = list_objects(fpath)
    print('Preview counted objects: {}'.format(counted2))
    print('Preview first object: {}'.format(listed2[0]))
    collection = set_collection(client, 'telus', 'awards')
    fmoid, _ = add_test(collection, listed2)
    print('Inserted objects: {}'.format(collection.count()))
    rdict_fmoid = collection.find_one({'_id':ObjectId(fmoid)})
    jdict_fmoid = json.dumps(rdict_fmoid, default=json_util.default)
    print('Inserted first object: {}'.format(jdict_fmoid))
