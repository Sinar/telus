#!/usr/bin/python
"""
This is the main script for telus.

telus is a project implemented in Python. The codes are developed
using Python 2.7 to be compatible with most Python frameworks and
Python packages in older systems with long term support.

The code syntax shall be as much as compatible with Python 3.
"""

from __future__ import print_function

import sys
import os
import fnmatch
import lib.jsonl
import pymongo

def check_env():
    """Return strings of Python version, system platform."""
    xyz, _ = sys.version.split(' ', 1)
    sps = sys.platform
    return xyz, sps

def list_files(spath, blob):
    """Return path, list, count of files with specified type."""
    slist = []
    scount = 0
    for fname in os.listdir(spath):
        if fnmatch.fnmatch(fname, blob):
            scount = scount + 1
            print('Found {}'.format(fname))
            slist.append(fname)
    return spath, slist, scount

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
    else:
        print('Connected to server')

def main():
    """The main function and default route for app."""
    print('Hello, telus!')
    version, platform = check_env()
    print('Using Python {0} on {1}'.format(version, platform))
    spath, listed, counted = list_files('./data', '*.jsonl')
    print('JSONL files found: {}'.format(counted))
    lib.jsonl.scan_jsonl(spath, listed, counted)
    test_conn()

if __name__ == '__main__':
    main()
