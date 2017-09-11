#!/usr/bin/python
"""
This is the main script for telus.

telus is a project implemented in Python. The codes are developed
using Python 2.7 to be compatible with most Python frameworks and
Python packages in older systems with long term support.

The code syntax shall be as much as compatible with Python 3.
"""

from __future__ import print_function

import lib.query
import lib.jsonl
import lib.pymg3

def dry_run():
    """Print information without making any changes."""
    lib.query.print_env()
    lib.query.print_files('./data', '*')
    lib.jsonl.scan_jsonl('./data')
    lib.pymg3.test_conn('localhost', 27017)

def test_awards():
    """Test store awards using basic operations."""
    fpath = './data/jkr-keputusan_tender.jsonl'
    lib.jsonl.test_one(fpath)
    lib.jsonl.show_line(fpath, 1)
    client = lib.pymg3.use_conn('localhost', 27017)
    _, awards = lib.pymg3.use_setup(client, 'telus', 'awards')
    lib.pymg3.drop_objects(awards)
    lib.pymg3.store_nested(client, awards, fpath)
    lib.pymg3.show_nested(client, awards)

def main():
    """Default function for main script."""
    print('Hello, telus!')
    try:
        test_awards()
    except IOError as error:
        detail = error
    except ValueError as error:
        detail = error
    except RuntimeError as error:
        detail = error
    except Exception as error:
        detail = error
        raise
    else:
        detail = 'Done'
    finally:
        print(detail)

if __name__ == '__main__':
    print('Execute {}'.format(__file__))
    main()
else:
    print('Import {}'.format(__file__))
