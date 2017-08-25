#!/usr/bin/python
"""
This is the main script for telus.

telus is a project implemented in Python. The codes are developed
using Python 2.7 to be compatible with most Python frameworks and
older systems with long term support.

The code syntax shall be as much as compatible with Python 3.
"""

from __future__ import print_function

import sys
import os
import fnmatch
import json

def check_env():
    """Return Python version and system platform."""
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

def test_one(spath, fname):
    """Test one JSONL file."""
    try:
        full_path = spath + '/' + fname
        print('Read {}'.format(full_path))
        lines = 0
        for jobject in open(full_path, 'r'):
            lines = lines + 1
            json.loads(jobject)
        print('Parsed objects: {}'.format(lines))
    except:
        print('Unexpected JSON object, check the syntax')
        raise

def test_many(path, flist):
    """Test many JSONL files."""
    try:
        files = 0
        for fname in flist:
            files = files + 1
            test_one(path, fname)
        print('Parsed files in total: {}'.format(files))
    except:
        print('Bad JSON list file')
        raise

def scan_jsonl(spath, flist, fcount):
    """Decide whether to test one or many JSONL files."""
    if fcount == 1:
        print('Test the only file')
        test_one(spath, flist[0])
    elif fcount > 1:
        print('Test many files')
        test_many(spath, flist)
    else:
        print('Huh, something was wrong')
        sys.exit(1)

def main():
    """The main function and default route for app."""
    print('Hello, telus!')
    version, platform = check_env()
    print('Using Python {0} on {1}'.format(version, platform))
    spath, listed, counted = list_files('./telus-data', '*.jsonl')
    print('JSONL files found: {}'.format(counted))
    scan_jsonl(spath, listed, counted)
    print('All files contain valid JSON objects')

if __name__ == '__main__':
    main()
