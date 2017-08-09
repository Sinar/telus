#!/usr/bin/python

from flask import Flask
import sys
import json

app = Flask(__name__)

# requires 'import json'
def fopen():
    parse = json.load(open('data/test2.json','r'))
    print(parse) # verbose output
    return parse # type 'dict'

@app.route('/')
@app.route('/home')
# requires 'import json'
def main():
    data2 = fopen()
    data2 = json.dumps(data2, indent=4, sort_keys=True) # pretty
    print(data2) # verbose
    return data2

if __name__ == '__main__':
    app.run()
