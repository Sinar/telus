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
    """Print information without running any operations."""
    lib.query.print_env()
    lib.jsonl.scan_jsonl('./data')
    lib.pymg3.test_conn('localhost', 27017)

def test_awards():
    """Test store awards using basic operations."""
    client = lib.pymg3.use_conn('localhost', 27017)
    lib.pymg3.set_database(client, 'telus')
    lib.pymg3.store_awards(client,
                            './data/jkr-keputusan_tender.jsonl')

def main():
    """Default function for main script."""
    print('Hello, telus!')
    dry_run()
    test_awards()

if __name__ == '__main__':
    main()
