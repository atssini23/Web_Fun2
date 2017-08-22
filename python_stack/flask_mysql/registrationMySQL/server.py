from flask import Flask, render_template, session, flash,request,redirect
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key="shhhhhh"

@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/success')
def success ():
    emails = mysql.query_db("SELECT * FROM email")
    return render_template('success.html', emails=emails)

@app.route('/submit', methods=['POST'])
def submit ():
    is_valid = True
    email = request.form['email']

    if is_empty(email):
        flash("Email is required")
        is_valid = False

    if not EMAIL_REGEX.match(email):
        flash("Please enter valid email")
        is_valid = False

    if is_valid:
        mysql.query_db("""
            INSERT INTO email (email, created_at, updated_at)
            VALUES ("{}", NOW(), NOW());
        """.format(email));
        return redirect("/success")

    return render_template('index.html',email=email)

def is_empty(text):
    return text is None or text == ''

app.run(debug=True)
