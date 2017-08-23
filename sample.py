#!/usr/bin/python

from flask import Flask, request
import json

app = Flask(__name__)

def json_file(path):
    fopen = open(path,'r')
    fdata = json.load(fopen)
    return fdata

@app.route('/')
def main():
    return 'Hello Flask'

@app.route('/release/1',methods=['GET'])
def get_tender():
    parse = json_file('data/tender.json')
    data = app.response_class(
                response = json.dumps(parse),
                status = 200,
                mimetype = 'application/json')
    return data

@app.route('/release/2',methods=['GET'])
def get_award():
    parse = json_file('data/award.json')
    data = app.response_class(
                response = json.dumps(parse),
                status = 200,
                mimetype = 'application/json')
    return data
    
@app.route('/release/tender/title=<title>',methods=['GET'])
def get_tender_by_title(title):
    parse = json_file('data/release_test.json')
    if title == parse['tender']['title']:
        parse = parse['tender']
        status_code = 200
    else:
        parse = { "result": "Not found" }
        status_code = 404
    data = app.response_class(
                response = json.dumps(parse),
                status = status_code,
                mimetype = 'application/json')
    return data

if __name__ == '__main__':
    app.run()
