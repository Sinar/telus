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

from flask import Flask, json
import telus

APP = Flask(__name__)

@APP.route('/')
def home():
    """Default function for web script and main route for app."""
    msg = 'Hello, telus! from Flask'
    print(msg)
    return msg

@APP.route('/demo')
def demo():
    """Demonstrate running function from main script."""
    try:
        telus.dry_run()
    except ValueError as error:
        detail = error
        parse = {"result": "Failed to process"}
        status = 400 # Bad request
    except RuntimeError as error:
        detail = error
        parse = {"result": "Failed to connect"}
        status = 404 # Not found
    else:
        detail = 'Done'
        parse = {"result": "Successful"}
        status = 200 # OK
    finally:
        print(detail)
        result = APP.response_class(
                    response=json.dumps(parse),
                    status=status,
                    mimetype='application/json')
    return result

if __name__ == '__main__':
    APP.run()
