import json, urllib, os

from flask import Flask, render_template, flash, request, session, redirect, url_for

from utils import db as lamb
from utils import api
from random import choice

DB_FILE = "data/lambBaaas.db"
app = Flask(__name__)
user = None
app.secret_key = os.urandom(32)
data = lamb.DB_Manager(DB_FILE)

#_choice = ""
#search = ""
data.createUsers()
data.createTyping()
data.createVocab()

def setUser(userName):
    global user
    user = userName

@app.route('/', methods=['POST', 'GET'])
def home():
    '''
    Landing page.
    '''
    if user in session:
        data = lamb.DB_Manager(DB_FILE)
        return render_template('homepage.html', user_name = user, loggedin = "True")


    return render_template("homepage.html")

@app.route('/auth', methods=['POST'])
def auth():
    '''
    Authentication route. Reroutes to home route when authenticated.
    '''
    # instantiates DB_Manager with path to DB_FILE
    data = lamb.DB_Manager(DB_FILE)
    # LOGGING IN
    if request.form["action"] == "Login":
        username, password = request.form["username_login"], request.form['password_login']
        if username != "" and password != "" and data.verifyUser(username, password ) :
            session[username] = password
            setUser(username)
            data.save()
            return redirect(url_for('home'))
        # user was found in DB but password did not match
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()
        return redirect(url_for("home"))

@app.route('/create_account_action', methods=["POST"])
def create_account_action():
    '''
    Creates account. Reroutes to home when successful.
    '''
    data = lamb.DB_Manager(DB_FILE)
    username, password, password2 = request.form["username_reg"], request.form['password_reg'], request.form['password_check']
    if len(username.strip()) != 0 and not data.findUser(username):
        if len(password.strip()) != 0:
            # add the account to DB
            if password != password2:
                flash('Passwords must match')
            else:
                data.registerUser(username, password)
                data.save()
                flash('Created account')
                return redirect(url_for('home'))
        else:
            flash('Password needs to have stuff in it')
    elif len(username) == 0:
        flash("Username needs to have stuff in it")
    else:
        flash("Username already taken!")
    # TRY TO REGISTER AGAIN
    return render_template("homepage.html")

@app.route('/logout')
def logout():
    '''
    Logs the user out.
    '''
    session.pop(user, None)
    setUser(None)
    return redirect(url_for('home'))

@app.route('/activity')
def bored_activity():
    '''
    Boilerplate for bored API.
    '''
    activity = api.get_bored_activity()['activity']
    return activity

# @app.route('/return')
# def ret():
#     return redirect(url_for('home'))

if (__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
