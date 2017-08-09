#!/usr/bin/python

from flask import Flask, Response
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
# requires 'from flask import Response'
def main():
    data4 = fopen()
    data4 = Response(response=json.dumps(data4),
            status=200,
            mimetype="application/json")
    return data4

if __name__ == '__main__':
    app.run()
