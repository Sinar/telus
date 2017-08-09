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
# requires 'import json' or 'from flask import json'
def main():
    data3 = fopen()
    data3 = app.response_class(
            response = json.dumps(data3),
            status = 200,
            mimetype = 'application/json')
    return data3

if __name__ == '__main__':
    app.run()
