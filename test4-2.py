#!/usr/bin/python

from flask import Flask
import requests
import json
import sqlite3 as sql

app = Flask(__name__)

def json_whole():
    whole = { "result": [] }
    return whole

def json_entry():
    entry =  { "id": {},
               "person": { "name": {}, "gender": {} },
               "organization": { "name": {} },
               "post": { "role": {} }
             }
    return entry

def api_query():
    mid = '545e621b5222837c2c05a806'
    url = 'http://api.popit.sinarproject.org/en/memberships/' + mid
    print('Query data from {0}...'.format(url))
    req = requests.get(url)
    dat = req.json() # return similar to Popit API
    return dat

def json_data():
    data = api_query() # single query contains nested 'dict', not 'list'!
    return data

def base_connect():
    return sql.connect('test4-2.db')

def base_setup():
    try:
        base = base_connect()
        cursor = base.cursor()
        cursor.execute("DROP TABLE IF EXISTS table4") # redo at run
        cursor.execute("CREATE TABLE IF NOT EXISTS table4 \
            (pid, name, gen, org, pos)")
        base.commit()
        print('CREATE was successful')
        data = json_data() #  read as 'dict'
        data_r = data['result'] # look into nested 'dict'
        entry = data_r # 'dict' doesn't need to loop, access directly
        cursor.execute("INSERT INTO table4 VALUES (?, ?, ?, ?, ?)",
            (entry['id'],
             entry['person']['name'],
             entry['person']['gender'],
             entry['organization']['name'],
             entry['post']['role']))
        base.commit()
        print('INSERT was successful')
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
        base = base_connect()
        cursor = base.cursor()
        cursor.execute("SELECT * FROM table4") # entire data
        #cursor.execute("SELECT * FROM table4 WHERE name = ?",
        #    ('Thomas Edison',)) # filter data by target name
        # note that this ^^^ last comma is needed, else syntax error
        rows = cursor.fetchall()
        print('SELECT was successful')
    except:
        base.rollback()
        msg = 'Read has failed'
        print(msg)
    finally:
        # don't close database here, other function will use afterwards
        msg = 'Read has completed'
        print(msg)
    return rows

def base_dump():
    try:
        base = base_connect()
        rows = base_read()
        print('SELECT was successful')
        new = json_whole() # a complete dict which has an empty list
        new_list = new['result'] # deal only with the list
        for entry in rows:
            new_ent = json_entry() # reset new entry at every time
            print('Parse entry:\n{0}'.format(entry)) # verbose
            new_ent['id'] = entry[0]
            new_ent['person']['name'] = entry[1]
            new_ent['person']['gender'] = entry[2]
            new_ent['organization']['name'] = entry[3]
            new_ent['post']['role'] = entry[4]
            print('Append entry to list:\n{0}'.format(new_ent)) # verbose
            new_list.append(new_ent)
        print('Append was successful')
    except:
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
def main():
    print('Input JSON data from file:')
    source = json_data()
    source_pretty = json.dumps(source, indent=4, sort_keys=True)
    print(source_pretty) # preview input JSON data
    print('Save JSON data into database...')
    base_setup() # create database first
    print('Read JSON data from database...')
    result = base_dump() # save input JSON data into database, then return
    print('Output JSON data:')
    result_pretty = json.dumps(result, indent=4, sort_keys=True)
    print(result_pretty) # output JSON data should appear same as input
    result = app.response_class(
                response = json.dumps(result),
                status = 200,
                mimetype = 'application/json')
    print('Output response:')
    print(result) # only response status will be printed here
    return result # return JSON data as object

if __name__ == '__main__':
    app.run()
