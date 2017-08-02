#!/usr/bin/python

from flask import Flask, render_template, request
import sys
import json
import sqlite3 as sql

app = Flask(__name__)

def connect():
    return sql.connect("test1.db") # factorize code

@app.route('/')
@app.route('/home')
def home():
    txt = "Hello, Flask!"
    return render_template("test1.html", msg = txt)

@app.route('/create')
def new():
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS \
                example(id,firstname,lastname,titlepos,titledep)")
    except:
        con.rollback()
        txt = "Something has failed"
    finally:
        txt = "CREATE was successful"
        return render_template("test1.html", msg = txt)

@app.route('/delete')
def delete():
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS example")
            con.commit()
    except:
        con.rollback()
        txt = "Something has failed"
    finally:
        txt = "DELETE was successful"
        return render_template("test1.html", msg = txt)

@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    if request.method == 'GET':
        try:
            parse = json.load(open('data/test1.json','r'))
            print(parse) # verbose output
            with connect() as con:
                cur = con.cursor()
                for item in parse['data']:
                    cur.execute("INSERT INTO \
                    example(id,firstname,lastname,titlepos,titledep) \
                    VALUES (?,?,?,?,?)",(item['id'],
                    item['name']['first'],item['name']['last'],
                    item['title']['position'],
                    item['title']['department']))
                con.commit()
                txt = "INSERT was successful"
        except:
            con.rollback()
            txt = "Something has failed"
        finally:
            return render_template("test1.html", msg = txt)
            con.close()
    else:
        return 'If you see this, something wrong with the method'
        # note: use 'POST' when submit via form or command

@app.route('/select')
def select():
    try:
        con = connect()
        con.row_factory = sql.Row # optimized type for easier access
        cur = con.cursor()
        cur.execute("SELECT * FROM example")
        rows = cur.fetchall()
        for row in rows:
            print(row) # verbose output
        txt = "SELECT was successful"
    except:
        con.rollback()
        txt = "Something has failed"
    finally:
        return render_template("result1.html", ent = rows, msg = txt)

if __name__ == '__main__':
    app.run()
