from flask import Flask, render_template, session, flash, request, redirect
import re
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
app.secret_key="shhhhhh"

@app.route('/')
def index ():
    registration = mysql.query_db("SELECT * FROM registration")
    return render_template('index.html')

@app.route('/complete/<id>')
def show(id):
    query = "SELECT * FROM registration WHERE id = :specific_id"
    data ={'specific_id': id}
    registration = mysql.query_db(query,data)
    return render_template('complete.html',one_registration=registration[0])

@app.route('/complete', methods=['POST'])
def submit ():
    is_valid = True
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']
    password = request.form['password']
    cpassword = request.form['cpassword']
    if is_empty(email):
        flash("Email is required")
        is_valid = False
    if is_empty(fname):
        flash("Name is required")
        is_valid = False
    if is_empty(lname):
        flash("Last Name is required")
        is_valid = False
    if is_empty(password):
        flash("Password is required")
        is_valid = False
    if is_empty(cpassword):
        flash("Confirm password")
        is_valid = False

    if not str.isalpha(str(fname)) or not str.isalpha(str(lname)):
        flash("Names can only contain letters")
        is_valid = False
    if len('fname') and len('lname')<2:
        flash("Name must contain more characters")
        is_valid = False
    if len(password)<8:
        flash("Password must contain 8 characters")
        is_valid = False
    if not EMAIL_REGEX.match(email):
        flash("Please enter valid email")
        is_valid = False
    if password != cpassword:
        flash("Passwords do not match!")
        is_valid = False

    hash_pw= bcrypt.generate_password_hash(password, 10)
    print hash_pw

    if is_valid:
        query ="INSERT INTO registration (email, fname, lname, password, created_at, updated_at) VALUES (:email, :fname, :lname, :password, NOW(), NOW())"
        data ={
                'email': request.form['email'],
                'fname': request.form['fname'],
                'lname': request.form['lname'],
                'password': hash_pw
                }
        id = mysql.query_db(query,data)
        return redirect('/complete/'+str(id))

    return redirect('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    query = 'SELECT * FROM registration WHERE email=:email'
    data = {
        'email':email
    }
    user = mysql.query_db(query,data)[0]

    hash_pw = bcrypt.generate_password_hash(password, 10)

    if bcrypt.check_password_hash(user['password'], hash_pw):
        flash('Invalid password')
        return redirect('/')
    return redirect('/complete/'+ str(user['id']))
def is_empty(text):
    return text is None or text == ''

app.run(debug=True)
