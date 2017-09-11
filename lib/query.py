#!/usr/bin/python
"""
This is a module for dealing with queries.

Use this module to look up details of system environment, including
the version number of Python interpreter, the system on which Python
is running, and other details that are needed for some operations.
"""

from __future__ import print_function

import sys
import os
import fnmatch

def get_version():
    """Return the version number of Python interpreter."""
    xyz, _ = sys.version.split(' ', 1)
    return xyz

def get_platform():
    """Return the identity of system on which Python is running."""
    sps = sys.platform
    return sps

def print_env():
    """Print information of system environment."""
    version = get_version()
    platform = get_platform()
    print('Using Python {0} on {1}'.format(version, platform))

def list_files(spath, blob):
    """Return list of files with specified type."""
    name_ls = []
    for name in os.listdir(spath):
        if fnmatch.fnmatch(name, blob):
            name_ls.append(name)
    return name_ls

def print_files(spath, blob):
    """
    Print list and number of files of specified type at given path.
    This is to demonstrate use of manual counter for numbering the
    print messages and use of function for built-in type of sequence
    that doesn't require to count each by loop.
    """
    file_ls = list_files(spath, blob)
    print('Found the following files:')
    count = 0
    for each in file_ls:
        count = count + 1
        print('File {0}: {1}'.format(count, each))
    file_num = len(file_ls)
    print('Total files: {}'.format(file_num))

def list_objects(fpath):
    """Return list of objects from specified file."""
    obj_ls = []
    for obj in open(fpath, 'r'):
        obj_ls.append(obj)
    return obj_ls
