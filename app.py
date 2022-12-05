import os
import random
import requests
from datetime import datetime
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_simple_geoip import SimpleGeoIP
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

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


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects/com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function



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
@login_required
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
@login_required
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
@login_required
def daily():

    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    
    # POST request
    if request.method == 'POST':

        # Save changes to task lists complete/incomplete
        if 'save-daily' in request.form:

            # Get date value from form input
            if request.form.get('date'):
                today = request.form.get('date').split('-')
                day, month, year = today[2], today[1], today[0]

            rows = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND month = (?) AND day = (?) AND frequency = (?) OR frequency = (?)", session['user_id'], year, month, day, 'today', 'everyday')

            # Iterate thru each checkbox and update db if checked off
            checked = request.form.getlist('checkbox')

            # Set to incomplete if not checked or unchecked
            for row in rows:
                if row['task_id'] not in checked:
                    db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'incomplete', row['task_id'])

            # checked = ['task_id', 'task_id',...]
            for task in checked:
                # Set to complete if task is checked
                db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'complete', task)


            # Render template after updating all db
            username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

            daily = db.execute("SELECT * FROM todo WHERE id = (?) AND day = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], day, month, year, 'today') 
            everyday = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'everyday')

            return render_template('daily.html', username=username, daily=daily, everyday=everyday, day=day, month=month, year=year)


        # ADD task form POST
        elif 'daily-submit' in request.form:

            username = db.execute("SELECT username FROM users WHERE id = (?)", session['user_id'])[0]['username']
            
            task = request.form.get('daily')
            frequency = request.form.get('goal-type')

            db.execute("INSERT INTO todo (id, task, frequency, completeness, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)", session['user_id'], task, frequency, 'incomplete', day, month, year)

            daily = db.execute("SELECT * FROM todo WHERE id = (?) AND day = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], day, month, year, 'today') 
            everyday = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'everyday')

            return render_template('daily.html', username=username, daily=daily, everyday=everyday, day=day, month=month, year=year)



        # REMOVE task form POST
        elif 'remove-submit' in request.form:

            removed = request.form.get('remove')
            db.execute("DELETE FROM todo WHERE task_id = (?)", removed)

            # Render template after updating all db
            username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

            daily = db.execute("SELECT * FROM todo WHERE id = (?) AND day = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], day, month, year, 'today') 
            everyday = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'everyday')

            return render_template('daily.html', username=username, daily=daily, everyday=everyday, day=day, month=month, year=year)


    # GET request
    elif request.method == "GET":

        # Pull info from db for menu
        id = session['user_id']
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        daily = db.execute("SELECT * FROM todo WHERE id = (?) AND day = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], day, month, year, 'today') 
        everyday = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'everyday')

        return render_template('daily.html', username=username, daily=daily, everyday=everyday, day=day, month=month, year=year)




@app.route('/monthly', methods=['GET', 'POST'])
@login_required
def monthly():

    today = datetime.now()
    today_month = today.month
    year = today.year

    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    MONTH = months[int(today_month) - 1]

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

        month = db.execute("SELECT * FROM todo WHERE id = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], today_month, year, 'month') 
        monthly = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'monthly')

        return render_template('monthly.html', username=username, month=month, monthly=monthly, MONTH=MONTH, year=year)


    # POST request
    elif request.method == 'POST':

        # ADD goals for month POST
        if 'monthly-submit' in request.form:

            task = request.form.get('monthly')
            frequency = request.form.get('goal-type')

            db.execute("INSERT INTO todo (id, task, frequency, completeness, month, year) VALUES (?, ?, ?, ?, ?, ?)", session['user_id'], task, frequency, 'incomplete', today_month, year)

            username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

            month = db.execute("SELECT * FROM todo WHERE id = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], today_month, year, 'month') 
            monthly = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'monthly')

            return render_template('monthly.html', username=username, month=month, monthly=monthly, MONTH=MONTH, year=year)


        # REMOVE goals for month POST
        elif 'remove-submit' in request.form:

            removed = request.form.get('remove')
            db.execute("DELETE FROM todo WHERE task_id = (?)", removed)

            username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

            month = db.execute("SELECT * FROM todo WHERE id = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], today_month, year, 'month') 
            monthly = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'monthly')

            return render_template('monthly.html', username=username, month=month, monthly=monthly, MONTH=MONTH, year=year)


        # SAVE completeness status changes
        elif 'save-daily' in request.form:

            if request.form.get('date'):
                today = request.form.get('date').split('-')
                month, year = today[1], today[0]

            rows = db.execute("SELECT * FROM todo WHERE id = (?) AND month = (?) AND year = (?) AND frequency = (?) OR frequency = (?)", session['user_id'], today_month, year, 'month', 'monthly')

            # Iterate thru each checkbox and update db if checked off
            checked = request.form.getlist('checkbox')

            # Set to incomplete if not checked or unchecked
            for row in rows:
                if row['task_id'] not in checked:
                    db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'incomplete', row['task_id'])

            # checked = ['task_id', 'task_id',...]
            for task in checked:
                # Set to complete if task is checked
                db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'complete', task)

            # Render template after updating all db
            username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

            month = db.execute("SELECT * FROM todo WHERE id = (?) AND month = (?) AND year = (?) AND frequency = (?)", session['user_id'], today_month, year, 'month') 
            monthly = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'monthly')

            return render_template('monthly.html', username=username, month=month, monthly=monthly, MONTH=MONTH, year=year)



@app.route('/yearly', methods=['GET', 'POST'])
@login_required
def yearly():

    id = session['user_id']
    today = datetime.now()
    this_year = today.year

    # GET request
    if request.method == "GET":

        # Pull info from db for menu
        username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

        year = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND frequency = (?)", session['user_id'], this_year, 'year')
        annual = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'annual')

        return render_template('yearly.html', username=username, year=year, annual=annual, this_year=this_year)

    
    # POST request
    elif request.method == 'POST':

        # ADD goals for year POST
        if 'yearly-submit' in request.form:

            task = request.form.get('annually')
            frequency = request.form.get('goal-type')

            db.execute("INSERT INTO todo (id, task, frequency, completeness, year) VALUES (?, ?, ?, ?, ?)", session['user_id'], task, frequency, 'incomplete', this_year)

            username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

            year = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND frequency = (?)", session['user_id'], this_year, 'year')
            annual = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'annual')

            return render_template('yearly.html', username=username, year=year, annual=annual, this_year=this_year)

        
        # REMOVE task form POST
        elif 'remove-submit' in request.form:

            removed = request.form.get('remove')
            db.execute("DELETE FROM todo WHERE task_id = (?)", removed)

            username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

            year = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND frequency = (?)", session['user_id'], this_year, 'year')
            annual = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'annual')

            return render_template('yearly.html', username=username, year=year, annual=annual, this_year=this_year)



        # SAVE completeness status changes
        elif 'save-daily' in request.form:

            if request.form.get('date'):
                today = request.form.get('date').split('-')
                this_year = today[0]

            rows = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND frequency = (?) OR frequency = (?)", session['user_id'], this_year, 'year', 'annual')

            # Iterate thru each checkbox and update db if checked off
            checked = request.form.getlist('checkbox')

            # Set to incomplete if not checked or unchecked
            for row in rows:
                if row['task_id'] not in checked:
                    db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'incomplete', row['task_id'])

            # checked = ['task_id', 'task_id', ...]
            for task in checked:
                # Set to complete if task is checked
                db.execute("UPDATE todo SET completeness = (?) WHERE task_id = (?)", 'complete', task)

            # Render template after updating all db
            username = db.execute("SELECT username FROM users WHERE id = ?", id)[0]['username']

            year = db.execute("SELECT * FROM todo WHERE id = (?) AND year = (?) AND frequency = (?)", session['user_id'], this_year, 'year')
            annual = db.execute("SELECT * FROM todo WHERE id = (?) AND frequency = (?)", session['user_id'], 'annual')

            return render_template('yearly.html', username=username, year=year, annual=annual, this_year=this_year)
