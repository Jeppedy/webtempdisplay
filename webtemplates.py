#!/usr/bin/env python

import sqlite3
from flask import Flask
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash
app = Flask(__name__)

# configuration
DATABASE = '/media/USBHDD1/TempMonData/rfmonDB.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html') 

@app.route("/")
def withTemplate():
    WHERE=""
    node = request.args.get('node') 
    if node is not None and node != "all":
        WHERE += "and nodeid=\'"+node+"\'"
    else: 
        node="all"

    metricguid = request.args.get('metricguid') 
    if metricguid is not None and metricguid != "all":
        WHERE += "and metricguid=\'"+metricguid+"\'"
    else: 
        metricguid="all"

    if( WHERE is not None ):
        # Remove initial "and" 
        WHERE = WHERE.replace( "and ", "where ", 1)

    numrows = request.args.get('numentries') 
    if numrows is None:
	numrows="50"

    curs = g.db.execute("select distinct nodeid, nodedescription from xmitters order by 1")
    nodelist = curs.fetchall()

    curs = g.db.execute("select distinct metricguid, metricname from rawdata order by 1")
    nodetypelist = curs.fetchall()

    curs = g.db.execute("select nodeid, metricname, metric, metricdt from rawdata "+WHERE+" order by metricdt desc limit "+numrows)
    entries = curs.fetchall()

    return render_template('metrics_table.html', nodelist=nodelist, nodetypelist=nodetypelist, entries=entries, node=node,  metricguid=metricguid, maxrows=numrows) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)

