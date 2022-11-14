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

                return redirect('/first')


        # LOGIN POST REQUEST
        elif "login-submit" in request.form:
            return render_template('weather.html')


    # User routes via GET
    else:
        return render_template('index.html')


@app.route('/weather')
#@login_required
def weather():

    if request.method == 'GET':
        return render_template('weather.html')

