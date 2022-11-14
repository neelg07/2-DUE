import os
import datetime

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
            if len(rows) != 0:
                error = "Username already taken!"
                return render_template('error.html', error=error)

            else:
                # Log username and password(hashed) into db and give security code
                return redirect('/weather')


        # LOGIN POST REQUEST
        elif "login-submit" in request.form:
            return redirect('/weather')


    # User routes via GET
    else:
        return render_template('index.html')


@app.route('/weather')
#@login_required
def weather():

    if request.method == 'GET':
        return render_template('weather.html')

