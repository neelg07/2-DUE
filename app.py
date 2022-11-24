import os
import datetime
import random
import requests
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_simple_geoip import SimpleGeoIP
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

'''
# GeoLocation API 
app.config.update(GEOIPIFY_API_KEY='at_5YbZtjhPtJLUKvFsTDAaT5GwF4rAM')
simple_geoip = SimpleGeoIP(app)
'''

# Weather API
api_key = '83aa04568f1067d6494cb2be34cfb172'


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
            
            username = request.form.get('Username').rstrip()


            # Ensure username is unique in database
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)

            # If username is taken
            if len(rows) != 0:
                error = "Username already taken!"
                return render_template('error.html', error=error)


            else:
                # Log username and password(hashed) into db and give security code
                username = request.form.get('Username').rstrip()
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
            username = request.form.get('username').rstrip()
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



        # Forgot Password POST Request
        elif 'forgot-password' in request.form:

            # Check if code is same as code stored in user db
            code_input = request.form.get('forgot-code')
            user_input = request.form.get('forgot-user')

            rows = db.execute("SELECT * FROM users WHERE username = (?) AND security_code = (?)", user_input, code_input)

            # Code does not match
            if len(rows) != 1: 
                error = 'Invalid Username or Security Code!'
                return render_template('error.html', error=error)

            # Code/username match / check if passwords match
            if request.form.get('pass-reset') != request.form.get('verify-pass-reset'):
                error = 'Passwords do not match!'
                return render_template('error.html', error=error)

            # Everything works out / change password / update db
            else:
                password = request.form.get('pass-reset')
                hash = generate_password_hash(password)
                
                db.execute("UPDATE users SET hash = (?) WHERE username = (?)", hash, user_input)

                return redirect('/')
                

    # User routes via GET
    else:
        return render_template('index.html')




@app.route('/weather', methods=['GET', 'POST'])
#@login_required
def weather():

    if request.method == 'GET':

        username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

        # Shorten username if needed
        if len(username) >= 10:
            username = f'{username[0:7]}...'

        '''
        # Get geolocation of user for weather
        geoip_data = simple_geoip.get_geoip_data()
        '''
        return render_template('weather.html', username=username)

    elif request.method == 'POST':

        username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

        # Shorten username if needed
        if len(username) >= 10:
            username = f'{username[0:7]}...'

        city = request.form.get('City')

        weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}')

        # Invalid city input
        if weather_data.json()['cod'] == '404':
            city = 'Invalid City'

            return render_template('weather.html', username=username, city=city)

        # Valid city input
        else:
            weather = weather_data.json()['weather'][0]['main']
            temp = round(weather_data.json()['main']['temp'])
            icon = weather_data.json()['weather'][0]['icon']
            description = weather_data.json()['weather'][0]['description']

            return render_template('weather.html', username=username, city=city, weather=weather, temp=temp, description=description, icon=icon)



@app.route('/account', methods=['GET', 'POST'])
#@login_required
def account():

    # GET request 
    if request.method == 'GET': 

        # Pull info from db for menu bar
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']
        code = db.execute("SELECT security_code FROM users WHERE id = ?", id)[0]['security_code']

        return render_template('account.html', username=username, code=code)


    # POST request
    elif request.method == 'POST':

        # Change Username Post
        if 'change-user' in request.form:
            
            new_user = request.form.get('new-user')
            db.execute("UPDATE users SET username = (?) WHERE id = (?)", new_user, session['user_id'])

            return redirect('/account')

        # Change Password Post 
        elif 'change-pass' in request.form:

            password = request.form.get('new-pass')
            hash = generate_password_hash(password)
            db.execute("UPDATE users SET hash = (?) WHERE id = (?)", hash, session['user_id'])

            return redirect('/account')

        # Delete Account Post
        elif 'delete-account' in request.form:

            db.execute("DELETE FROM users WHERE id = ?", session['user_id'])

            return redirect('/logout')



@app.route('/logout')
def logout():

    # Forget any user_id
    session.clear()

    #Redirect user to login form
    return redirect('/')



@app.route('/daily', methods=['GET', 'POST'])
#@login_required
def daily():

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        daily = db.execute("SELECT * FROM tasks WHERE id = (?) AND frequency = (?)", session['user_id'], 'today') 
        everyday = db.execute("SELECT * FROM tasks WHERE id = (?) AND frequency = (?)", session['user_id'], 'everyday')

        return render_template('daily.html', username=username, daily=daily, everyday=everyday)

    
    # POST request
    elif request.method == 'POST':

        task = request.form.get('daily')
        frequency = request.form.get('goal-type')

        db.execute("INSERT INTO tasks (id, task, frequency, completeness) VALUES (?, ?, ?, ?)", session['user_id'], task, frequency, 'incomplete')

        return redirect('/daily')



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