#!/usr/bin/python

from flask import Flask
import sys
import requests
import json

app = Flask(__name__)

def aread():
    mid = '545e621b5222837c2c05a806'
    url = 'http://api.popit.sinarproject.org/en/memberships/' + mid
    print('Get details from {0}...'.format(url))
    req = requests.get(url)
    dat = req.json() # return similar to Popit API
    #dat = req.json()['result'] # return without top element 'result'
    return dat

def amend():
    parse = aread()
    if parse['result']['language_code'] == "en":
        print('English is used')
        parse['result']['test_field'] = "Something new"
    else:
        print('Nothing new to see')
    return parse

@app.route('/')
@app.route('/home')
def home():
    result = amend()
    print(result) # verbose
    result = app.response_class(
                response = json.dumps(result),
                status = 200,
                mimetype = 'application/json')
    return result

if __name__ == '__main__':
    app.run()
