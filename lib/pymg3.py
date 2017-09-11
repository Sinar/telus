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
    """Return list of objects from specified file."""
    obj_ls = []
    for each in open(fpath, 'r'):
        obj_ls.append(each)
    return obj_ls

def drop_objects(collection):
    """Remove all objects from specified collection if not empty."""
    if collection.count() != 0:
        print('{} was not empty, drop first'.format(collection.name))
        collection.drop()

def find_object(collection):
    """
    Return one JSON object from specified collection.
    """
    obj = collection.find_one()
    parse = json.dumps(obj, default=json_util.default, sort_keys=True)
    return parse

def find_objects(collection, args):
    """Return JSON objects from specified collection if any."""
    print('Query argument: {}'.format(args))
    obj_ls = []
    if type(args) is type({}):
        obj = collection.find(args)
        obj = list(obj)
        count = 0
        for each in obj:
            count = count + 1
            parse = json.dumps(each, default=json_util.default,
                                sort_keys=True)
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
        raise TypeError('Unexpected type of argument', type(args))

def show_object(collection):
    """
    Show one JSON object from specified collection in MongoDB. This
    depends on find_object function that return an object.
    """
    obj = find_object(collection)
    print('Show first object: {}'.format(obj))

def show_objects(collection, args):
    """Show JSON objects from specified collection in MongoDB."""
    obj = find_objects(collection, args)
    if type(obj) is type(''):
        print('Show target object: {}'.format(obj))
    elif type(obj) is type([]):
        print('Show only first 3 objects:')
        num = 0
        for each in obj:
            print(each)
            num = num + 1
            if num == 3:
                break
    else:
        raise TypeError('Unexpected type of object', type(obj))

def scan_field(obj, string):
    """Match non-empty value for specified string in JSON object."""
    value = obj[string]
    ismatch = False
    if value != "":
        ismatch = True
    return ismatch

def copy_field(obj, string):
    """Return standalone object of specified string in JSON object."""
    value = obj[string]
    new_obj = {string: value}
    return new_obj

def store_objects(collection, fpath):
    """Store objects from JSONL into MongoDB."""
    print('Store objects into {}'.format(collection.name))
    obj_ls = list_objects(fpath)
    for each in obj_ls:
        obj = json.loads(each)
        result = collection.insert_one(obj)
        if collection.count() == 1:
            first_id = result.inserted_id
    print('Inserted objects: {}'.format(collection.count()))
    show_objects(collection, {'_id':ObjectId(first_id)})

def store_nested(client, collection, fpath):
    """
    Store objects and the contained nested objects from JSONL into
    MongoDB. The nested objects are expected to be found in objects
    from JSONL file and have been predefined (buyer, seller).
    """
    print('Store source objects and nested objects')
    buyers = set_collection(client, 'telus', 'buyers')
    drop_objects(buyers)
    sellers = set_collection(client, 'telus', 'sellers')
    drop_objects(sellers)
    obj_ls = list_objects(fpath)
    for each in obj_ls:
        obj = json.loads(each)
        buyer_string = 'offering_office' # non-OCDS
        if scan_field(obj, buyer_string):
            buyers.insert_one(copy_field(obj, buyer_string))
        seller_string = 'contractor' # non-OCDS
        if scan_field(obj, seller_string):
            sellers.insert_one(copy_field(obj, seller_string))
        collection.insert_one(obj)
    print('Inserted buyers: {}'.format(buyers.count()))
    print('Inserted sellers: {}'.format(sellers.count()))
    print('Inserted source objects: {}'.format(collection.count()))
