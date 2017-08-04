#!/usr/bin/python

from flask import Flask, jsonify
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
# requires 'from flask import jsonify'
def json_literal():
    data1 = fopen()
    return jsonify(data1)

if __name__ == '__main__':
    app.run()
