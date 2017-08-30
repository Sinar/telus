#!/usr/bin/python
"""
This is the web framework script for telus.

Flask is a micro webdevelopment framework for Python, which is used
in this script. Whilst the codes are developed using Python 2, Flask
and most Flask extensions support Python 3 (Python 3.3 or higher).

For details, see Python 3 Support in Flask Documentation 0.12 for
stable release (http://flask.pocoo.org/docs/0.12/python3/).
"""

from __future__ import print_function

from flask import Flask

APP = Flask(__name__)

@APP.route('/')
def home():
    """Default function for web script and main route for app."""
    msg = 'Hello, telus! from Flask'
    print(msg)
    return msg

if __name__ == '__main__':
    APP.run()
