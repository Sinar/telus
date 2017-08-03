#!/usr/bin/python

from flask import Flask, render_template, request, jsonify, Response
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
def home():
    txt = "Hello, Flask!"
    return render_template("test2.html", msg = txt)

# requires 'from flask import jsonify'
@app.route('/json_literal')
def json_literal():
    data1 = fopen()
    return jsonify(data1)

# requires 'import json'
@app.route('/json_string')
def json_string():
    data2 = fopen()
    data2 = json.dumps(data2, indent=4, sort_keys=True) # pretty
    print(data2) # verbose
    return data2

# requires 'import json' or 'from flask import json'
@app.route('/json_rclass')
def json_rclass():
    data3 = fopen()
    data3 = app.response_class(
            response = json.dumps(data3),
            status = 200,
            mimetype = 'application/json')
    return data3

# requires 'from flask import Response'
@app.route('/json_respon')
def json_respon():
    data4 = fopen()
    data4 = Response(response=json.dumps(data4),
            status=200,
            mimetype="application/json")
    return data4

if __name__ == '__main__':
    app.run()
