import os
import datetime
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Config application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Config session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL('sqlite:///todo.db')


@app.after_request
def after_request(response):

    """Ensure responses aren't cached"""
    response.headers['Cache-Control'] = 'no-cache, no store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route("/", methods=['GET', 'POST'])
def index():
    
    # User routes via POST 
    if request.method == 'POST':

        # REGISTER POST REQUEST
        if "register-submit" in request.form:
            
            username = request.form.get('Username')


            # Ensure username is unique in database
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)

            # If username is taken
            if len(rows) != 0:
                error = "Username already taken!"
                return render_template('error.html', error=error)


            else:
                # Log username and password(hashed) into db and give security code
                username = request.form.get('Username')
                password = request.form.get('Password')

                # Generate hash for password storage in db
                hash = generate_password_hash(password)

                # Generate random 4 digit security code if user forgets password
                security_code = random.randint(1000,9999)

                db.execute("INSERT INTO users (username, hash, security_code) VALUES (?, ?, ?)", username, hash, security_code)

                # Create session id and login user 
                rows = db.execute("SELECT * FROM users WHERE username = ?", username)

                session['user_id'] = rows[0]['id']

                # Shorten username for menu bar if over 11 chars
                if len(username) >= 10:
                    username = f'{username[0:7]}...'

                return render_template('security.html', code=security_code, username=username)



        # LOGIN POST REQUEST
        elif "login-submit" in request.form:

            # Forget any user_id 
            session.clear()

            # Save login form entries into variables
            username = request.form.get('username')
            password = request.form.get('password')

            # Search database for matching entries
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            
            # Return error if username or password incorrect
            if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
                error = 'Invalid Username and/or Password!'
                return render_template('error.html', error=error)


            # Remember user session if valid login attempt
            session['user_id'] = rows[0]['id']

            # Redirect user to homepage // shorten username if necessary
            if len(username) >= 10:
                username = f'{username[0:7]}...'

            return render_template('weather.html', username=username)


    # User routes via GET
    else:
        return render_template('index.html')



@app.route('/weather')
#@login_required
def weather():

    if request.method == 'GET':

        username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

        # Shorten username if needed
        if len(username) >= 10:
                    username = f'{username[0:7]}...'

        return render_template('weather.html', username=username)



@app.route('/account')
#@login_required
def account():

    # GET request 
    if request.method == 'GET': 

        # Pull info from db for menu bar
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        return render_template('account.html', username=username)



@app.route('/logout')
def logout():

    # Forget any user_id
    session.clear()

    #Redirect user to login form
    return redirect('/')



@app.route('/daily')
#@login_required
def daily():

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        return render_template('daily.html', username=username)



@app.route('/monthly')
#@login_required
def monthly():

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        return render_template('monthly.html', username=username)



@app.route('/yearly')
#@login_required
def yearly():

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        return render_template('yearly.html', username=username)