#!/usr/bin/python

from flask import Flask
import json
import sqlite3 as sql

app = Flask(__name__)

def json_whole():
    whole = { "records": [] }
    return whole

def json_entry():
    entry = {
              "id": {},
              "company": {
                  "name": {},
                  "owner": {
                      "name": {},
                      "gender": {}
                  },
                  "partners": [
                  {
                      "name": {},
                      "gender": {}
                  }
                  ],
                  "status": {}
              }
            }
    return entry

def empty_record():
    new = json_whole()
    new_list = new['records']
    new_entry = json_entry()
    new_list.append(new_entry)
    return new_list

def json_data():
    data_file = open('data/test4-3.json','r')
    data = json.load(data_file)
    return data

def base_connect():
    return sql.connect('test4-3.db')

def base_setup():
    try:
        print('Setup begins')
        base = base_connect()
        cursor = base.cursor()
        cursor.execute("DROP TABLE IF EXISTS parent_table") # redo at run
        cursor.execute("CREATE TABLE IF NOT EXISTS parent_table \
            (parent_id, cname, coname, cogen, cstatus)")
        base.commit()
        print('Setup CREATE parent_table was successful')
        cursor.execute("DROP TABLE IF EXISTS child_table") # redo at run
        cursor.execute("CREATE TABLE IF NOT EXISTS child_table \
            (parent_id, pname, pgender)")
        base.commit()
        print('Setup CREATE child_table was successful')
        data = json_data() # read as 'dict'
        data_r = data['records'] # look into 'list'
        for entry in data_r:
            cursor.execute("INSERT INTO parent_table VALUES \
                 (?, ?, ?, ?, ?)",
                 (entry['id'],
                 entry['company']['name'],
                 entry['company']['owner']['name'],
                 entry['company']['owner']['gender'],
                 entry['company']['status']))
            nested_list = entry['company']['partners']
            for nested_entry in nested_list:
                cursor.execute("INSERT INTO child_table VALUES \
                    (?, ?, ?)",
                    (entry['id'],
                    nested_entry['name'],
                    nested_entry['gender']))
                base.commit()
            base.commit()
        print('Setup INSERT was successful')
    except Exception as e:
        print('Exception: {0}'.format(e)) # tell me what was wrong
        base.rollback()
        msg = 'Setup has failed'
        print(msg)
    finally:
        base.close()
        msg = 'Setup has completed'
        print(msg)
    return msg

def base_read():
    try:
        print('Read begins')
        base = base_connect()
        cursor = base.cursor()
        cursor.execute("SELECT * FROM parent_table")
        rows_parent = cursor.fetchall()
        cursor.execute("SELECT * FROM child_table")
        rows_child = cursor.fetchall()
        print('Read SELECT was successful')
    except Exception as e:
        print('Exception: {0}'.format(e)) # tell me what was wrong
        base.rollback()
        msg = 'Read has failed'
        print(msg)
    finally:
        # don't close database here, other function will use afterwards
        msg = 'Read has completed'
        print(msg)
    return rows_parent, rows_child

def base_dump():
    try:
        print('Dump begins')
        base = base_connect()
        rows_parent, rows_child = base_read()
        print('Dump SELECT was successful')
        new = json_whole() # a complete dict which has an empty list
        new_list = new['records'] # deal only with the list
        for entry in rows_parent:
            new_entry = json_entry() # reset new entry at every time
            #print('Parse entry:\n{0}'.format(entry)) # verbose
            new_entry['id'] = entry[0]
            new_entry['company']['name'] = entry[1]
            new_entry['company']['owner']['name'] = entry[2]
            new_entry['company']['owner']['gender'] = entry[3]
            new_entry['company']['status'] = entry[4]
            for subentry in rows_child:
                #print('Parse subentry:\n{0}'.format(subentry)) # verbose
                partners = new_entry['company']['partners']
                for partner in partners:
                    partner['name'] = subentry[1]
                    partner['gender'] = subentry[2]
            #print('Append entry to list:\n{0}'.format(new_entry)) # verbose
            new_list.append(new_entry)
        print('Dump append to list was successful')
    except Exception as e:
        print('Exception: {0}'.format(e)) # tell me what was wrong
        base.rollback()
        msg = 'Dump has failed'
        print(msg)
    finally:
        base.close()
        msg = 'Dump has completed'
        print(msg)
    return new # return as complete dict

@app.route('/')
@app.route('/home')
def home():
    print('Input JSON:')
    #empty = empty_record() # preview empty record of JSON data
    #print(empty)
    source = json_data()
    source_pretty = json.dumps(source, indent=4, sort_keys=True)
    print(source_pretty) 
    base_setup()
    parent_table, child_table = base_read()
    print('parent_table:\n{0}'.format(parent_table))
    print('child_table:\n{0}'.format(child_table))
    result = base_dump()
    print('Output JSON data:')
    result_pretty = json.dumps(result, indent=4, sort_keys=True)
    print(result_pretty)
    result = app.response_class(
                response = json.dumps(result),
                status = 200,
                mimetype = 'application/json')
    print('Output response:')
    print(result)
    return result
