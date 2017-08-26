#!/usr/bin/python
"""
This is a module for dealing with JSONL files.

Use this module to validate JSON objects in one or many JSONL files.
The validation make use of Python module `json`.
"""

from __future__ import print_function

import sys
import json

def test_one(spath, fname):
    """Test JSON objects in one JSONL file."""
    try:
        full_path = spath + '/' + fname
        print('Read {}'.format(full_path))
        lines = 0
        for jobject in open(full_path, 'r'):
            lines = lines + 1
            json.loads(jobject)
        print('Tested valid objects: {}'.format(lines))
    except:
        print('Unexpected JSON object, check the syntax')
        raise

def test_many(spath, flist):
    """Test JSON objects in many JSONL files."""
    files = 0
    for fname in flist:
        files = files + 1
        test_one(spath, fname)
    print('Parsed files in total: {}'.format(files))

def scan_jsonl(spath, flist, fcount):
    """Decide whether to parse one or many JSONL files."""
    if fcount == 1:
        print('Parse the only file')
        test_one(spath, flist[0])
    elif fcount > 1:
        print('Parse many files')
        test_many(spath, flist)
    else:
        print('Huh, something was wrong')
        sys.exit(1)
