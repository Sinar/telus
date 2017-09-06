#!/usr/bin/python
"""
This is a module for dealing with JSONL files.

Use this module to validate JSON objects in one or many JSONL files.
The validation make use of Python module `json`.
"""

from __future__ import print_function

import json
import os
import fnmatch

def test_obj(obj):
    """Test and return each JSON object."""
    try:
        obj = json.loads(obj)
    except ValueError:
        print('Unexpected JSON object, check the syntax')
        raise
    else:
        return obj

def test_line(fpath, lnum):
    """Test JSON object at specified line in JSONL file."""
    print('Read {}'.format(fpath))
    if type(lnum) is not type(0):
        raise TypeError('Unexpected type of line', type(lnum))
    elif lnum < 0:
        raise ValueError('Unexpected value of line', lnum)
    else:
        print('Look up line {}'.format(lnum))
    lines = 0
    for each in open(fpath, 'r'):
        lines = lines + 1
        if lines == lnum:
            parse = json.dumps(each)
            break
    # parse object as JSON formatted str, then convert to Python dict
    # end result is same as viewing in Web browser and Terminal
    obj = test_obj(parse)
    print('Preview target object: {}'.format(obj))

def test_one(fpath):
    """Test JSON objects in one JSONL file."""
    print('Read {}'.format(fpath))
    lines = 0
    for each in open(fpath, 'r'):
        lines = lines + 1
        test_obj(each)
    print('Tested valid objects: {}'.format(lines))

def test_many(spath, flist):
    """Test JSON objects in many JSONL files."""
    files = 0
    for fname in flist:
        files = files + 1
        fpath = spath + '/' + fname
        test_one(fpath)
    print('Parsed files in total: {}'.format(files))

def list_jsonl(spath):
    """Return list, count of JSONL files."""
    flist = []
    count = 0
    for fname in os.listdir(spath):
        if fnmatch.fnmatch(fname, '*.jsonl'):
            count = count + 1
            print('Found {0}: {1}'.format(count, fname))
            flist.append(fname)
    return flist, count

def scan_jsonl(spath):
    """Decide whether to parse one or many JSONL files."""
    flist, count = list_jsonl(spath)
    if count == 1:
        print('Parse the only file')
        fpath = spath + '/' + flist[0]
        test_one(fpath)
    elif count > 1:
        print('Parse many files')
        test_many(spath, flist)
    else:
        print('Did not parse')
        raise ValueError('Unexpected number of files found', count)
