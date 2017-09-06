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

def list_objects(fpath):
    """Return list, count of objects from specified file."""
    slist = []
    lines = 0
    for sobject in open(fpath, 'r'):
        lines = lines + 1
        slist.append(sobject)
    return slist, lines

def drop_objects(collection):
    """Remove all objects from specified collection if not empty."""
    if collection.count() == 0:
        pass
    else:
        print('Collection was not empty, drop first')
        collection.drop()

def find_objects(collection, jobject):
    """Return JSON objects from specified collection if any."""
    obj_ls = []
    if type(jobject) is type({}):
        obj = collection.find(jobject)
        obj = list(obj)
        count = 0
        for each in obj:
            count = count + 1
            parse = json.dumps(each, default=json_util.default)
            obj_ls.append(parse)
        if count == 0:
            print('Not found')
            return None
        elif count == 1:
            print('Found one object')
            return obj_ls[0]
        else:
            print('Found {} objects in a list'.format(count))
            return obj_ls
    else:
        print('Did not find')
        raise TypeError('Unexpected type of object', type(jobject))

def scan_field(jobject, jstring):
    """Match non-empty value for specified string in JSON object."""
    this_string = jstring
    this_value = jobject[this_string]
    ismatch = 'no'
    if this_value != "":
        ismatch = 'yes'
    return ismatch

def store_awards(client, fpath):
    """Store awards from JSONL into MongoDB."""
    print('Prepare to store awards')
    awards_ls, _ = list_objects(fpath)
    print('Preview first object: {}'.format(awards_ls[0]))
    _, awards = use_setup(client, 'telus', 'awards')
    drop_objects(awards)
    buyers_num = 0
    sellers_num = 0
    for each in awards_ls:
        jobject = json.loads(each)
        isbuyer = scan_field(jobject, 'offering_office') # non-OCDS
        if isbuyer != 'no':
            buyers_num = buyers_num + 1
        isseller = scan_field(jobject, 'contractor') # non-OCDS
        if isseller != 'no':
            sellers_num = sellers_num + 1
        result = awards.insert_one(jobject)
        awards_id = result.inserted_id
        if awards.count() == 1:
            first_id = awards_id
    print('Total non-empty buyers: {}'.format(buyers_num))
    print('Total non-empty sellers: {}'.format(sellers_num))
    print('Inserted objects: {}'.format(awards.count()))
    first_obj = find_objects(awards, {'_id':ObjectId(first_id)})
    print('Found first object: {}'.format(first_obj))
