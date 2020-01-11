#! usr/bin/python3

from flask import Flask, render_template, request, redirect, session
import sys
import os
import hashlib
from datetime import datetime
from doors import operate_door, get_door_status
from functools import wraps

app = Flask(__name__)

# Don't forget to define the environment varaibles!
app.secret_key = os.environ['SECRET_KEY']
garage_auth = os.environ['GARAGE_AUTH']

# Some basic authentication
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

# GARAGE_AUTH needs to be declared as an environment variable in the terminal
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    if request.method == 'POST':
        auth_hash = hashlib.sha256(request.form['auth_key'].encode())
        if auth_hash.hexdigest() == garage_auth:
            session['logged_in'] = True
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Returns current state of the doors. Open/close a door if requested.
    """
    # Get the last event from the log
    event_log = open('event.log', 'r')
    last_event = event_log.read()
    event_log.close()

    # If POST then operate the selected door and log the event time.
    if request.method == 'POST':
        door = request.form['door']
        operate_door(door)

    # Return the current door status regardless of whether GET or POST
    door_status = get_door_status()
    away = False
    if os.path.isfile('away'):
        away = True

    return render_template('index.html',
                            door_a=door_status[0],
                            door_b=door_status[1],
                            last_event=last_event, 
                            away=away)


# This routes is optional and works with notify.py and IFTTT to send
# an alert if a door is opened when the user is away from the house.
@app.route('/location', methods=['POST'])
def location():
    """
    IFTTT will access this url based on user location.
    If out of the area, an 'away' file is created.
    If local, the 'away' file is deleted.
    """
    # Key value passed by the IFTTT post
    key = request.get_json()['key']

    if key == 'ykNLS7HpkBjSBeT':
        if not os.path.isfile('away'):
            file = open('away', 'x')
            file.close()
        return 'Away Flag Active'

    if key == 'oFH4GuFQ7yCD8d4':
        if os.path.isfile('away'):
            os.remove('away')
        return 'Away Flag Removed'


# Run the app and make it accessible from the Interwebs
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)