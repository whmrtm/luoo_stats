from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
import requests
import string
import sqlite3
import json

app = Flask(__name__)




def get_db():
    return sqlite3.connect("luoo.db")




# Main page
@app.route('/')
@app.route('/display')
def showMain():
	cursor = get_db().cursor()
	rows = cursor.execute('select distinct tag from volume;').fetchall()
	tags =  []
	print(len(rows))
	for row in rows:
		tags.append(row[0].replace('#',''))
	tag_data = []
	for tag in tags:
	  r = cursor.execute("select distinct count(*) \
	  	from volume where tag='#"+tag+"';")
	  number = r.fetchone()[0]
	  tag_data.append({"tag":tag, "number":int(number)})


	return render_template('index.html', tag_data = json.dumps(tag_data))


@app.route('/search')
def showSearch():
	return render_template('search.html')

@app.route('/contact')
def showContact():
	return	render_template('contact.html')


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)



