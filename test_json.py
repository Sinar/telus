#!/usr/bin/python

import json

def json_file(path):
    fopen = open(path,'r')
    fdata = json.load(fopen)
    return fdata

parse = json_file('data/release_test.json')
if 'foo' == parse['tender']['title']:
    print('Found a match')
else:
    print('Not a match')
