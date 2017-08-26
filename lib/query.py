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
    """Return list, count of files with specified type."""
    slist = []
    scount = 0
    for fname in os.listdir(spath):
        if fnmatch.fnmatch(fname, blob):
            scount = scount + 1
            print('Found {}'.format(fname))
            slist.append(fname)
    return slist, scount

def list_objects(fpath):
    """Return list, count of objects from specified file."""
    slist = []
    lines = 0
    for sobject in open(fpath, 'r'):
        lines = lines + 1
        slist.append(sobject)
    return slist, lines
