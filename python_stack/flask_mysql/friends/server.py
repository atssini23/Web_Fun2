from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends')

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    return render_template('index.html', friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    name = request.form['name']
    age = request.form['age']

    result = mysql.query_db("""
        INSERT INTO friends (name, age, created_at, updated_at)
        VALUES ("{}", "{}", NOW(), NOW());
    """.format(name, age));

    print result;

    return redirect('/')
app.run(debug=True)
