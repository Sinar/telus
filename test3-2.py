#!/usr/bin/python

from flask import Flask
import sys
import requests
import json

app = Flask(__name__)

def fopen():
    dat = json.load(open('data/test3.json','r'))
    print(dat) # verbose
    return dat

def aread():
    mid = '545e621b5222837c2c05a806'
    url = 'http://api.popit.sinarproject.org/en/memberships/' + mid
    print('Get details from {0}...'.format(url))
    req = requests.get(url)
    dat = req.json() # return similar to Popit API
    return dat

def amend():
    source = fopen()
    print('source is {0}'.format(type(source))) # type 'dict'
    source = source['data']
    print('source data is {0}'.format(type(source))) # type 'list'
    parse = aread()
    parse_person = parse['result']['person']['name']
    for entry in source:
        source_person = entry['buyer']['name']
        if parse_person == source_person:
            print('Found a match: {0}'.format(parse_person))
            parse['result']['person_match'] = "True"
            break
        else:
            print('No match')
            parse['result']['person_match'] = "False"
    return parse

@app.route('/')
@app.route('/home')
def main():
    result = amend()
    print(result) # verbose
    result = app.response_class(
                response = json.dumps(result),
                status = 200,
                mimetype = 'application/json')
    return result

if __name__ == '__main__':
    app.run()
