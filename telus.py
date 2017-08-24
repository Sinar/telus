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

def check_env():
    """Return Python version and system platform."""
    xyz, _ = sys.version.split(' ', 1)
    sps = sys.platform
    return xyz, sps

def list_jsonl(path):
    """Return path, list and count of JSONL files."""
    jsonl_list = []
    blob = '*.jsonl'
    count = 0
    for fname in os.listdir(path):
        if fnmatch.fnmatch(fname, blob):
            count = count + 1
            print('Found {}'.format(fname))
            jsonl_list.append(fname)
    return path, jsonl_list, count

def scan_jsonl(flist, fcount):
    """Decide whether to test one or many JSONL files."""
    if fcount == 1:
        print('Test the only file: {}'.format(flist[0]))
        # test_one(spath, flist)
    elif fcount > 1:
        print('Test many files, found: {}'.format(fcount))
        # test_many(spath, flist)
    else:
        print('Huh, something was wrong')
        sys.exit(1)

def main():
    """The main function and default route for app."""
    print('Hello, telus!')
    version, platform = check_env()
    print('Using Python {0} on {1}'.format(version, platform))
    _, listed, counted = list_jsonl('./telus-data')
    print('JSONL files found: {}'.format(counted))
    scan_jsonl(listed, counted) # later: spath, listed, counted
    print('All files contain valid JSON objects')

if __name__ == '__main__':
    main()
