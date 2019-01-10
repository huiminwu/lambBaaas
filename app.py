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

def getText():
    F = open("data/hamlet.txt","r")
    text = F.read()
    return text

def setUser(userName):
    global user
    user = userName

@app.route('/', methods=['POST', 'GET'])
def home():
    '''
    Landing page.
    '''
    return render_template('homepage.html', loggingin = True)

@app.route('/wanna_register', methods=['POST', 'GET'])
def wanna_register():
    '''
    Landing page.
    '''
    return render_template('homepage.html', loggingin = False)

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
            return redirect(url_for('main'))
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

@app.route('/main', methods=['POST', 'GET'])
def main():
    '''
    Activities page.
    '''
    if user in session:
        data = lamb.DB_Manager(DB_FILE)
        return redirect(url_for('bored_activity'))

    return render_template("homepage.html")

@app.route('/activity')
def bored_activity():
    '''
    Boilerplate for bored API.
    '''
    activity = api.get_bored_activity()['activity']
    category = api.get_bored_activity()['type']
    return render_template("activity.html", act = activity, cat = category)

@app.route('/vocab', methods=['POST', 'GET'])
def vocab():
    '''
    Vocab home page.
    Displays all words, and an option to search for words.
    '''
    words = data.getVocabWords(user)
    print(words)
    return render_template('vocab.html', user_name = user, loggedin = "True")


@app.route('/wordSearch')
def word_activity():
    '''
    Displays a search query for words.
    '''
    return render_template("word_search.html")

@app.route('/wordResult', defaults={'word': None})
@app.route('/wordResult/<word>')
def search_results(word):
    '''
    Returns all entries for the word.
    Has an optional param for returning from the defintions endpoint.
    '''
    if word:
        query = word
    else:
        query = request.args['query']
        # checking for common mistakes
        query = query.strip()
        if query == '':
            flash('Input something valid!')
            return render_template("word_search.html")

    result = api.get_word(query)
    return render_template('word_search.html', **result)

@app.route('/def/<word>', defaults={'oldQuery': None})
@app.route('/def/<oldQuery>/<word>')
def definition(oldQuery, word):
    '''
    returns the definition of the selected word. Employs this through dynamic routing.
    if no defintions exist, user is returned to the previous page.
    '''
    result = api.get_definition(word)
    # save oldQuery in the result as well
    result['oldQuery'] = oldQuery
    if result == {}:
        flash('No definitions found!')
        if oldQuery:
            return redirect(url_for('search_results', word = oldQuery))
        return redirect(url_for('vocab'))
    return render_template('definitions.html', **result)

@app.route('/saveWord', methods = ['POST'])
def saveWord():
    '''
    Saves the input word to the DB. POST-only method.
    Redirects back to the old
    '''
    oldQuery = request.form['oldQuery']
    word = request.form['word']
    #print(oldQuery,word)
    data.saveWord(user, word)
    return redirect(url_for('definition', oldQuery = oldQuery, word = word))

# @app.route('/return')
# def ret():
#     return redirect(url_for('home'))

#@app.route('/activities', methods=['POST', 'GET'])
#def activities():
#    '''
#    Activities page.
#    '''
#    return render_template('activity.html', user_name = user, loggedin = "True")

@app.route('/typing', methods=['POST', 'GET'])
def typing():
    '''
    Typing page.
    '''
    return render_template('typing.html',
                            user_name = user,
                            loggedin = "True",
                            text = getText())

if (__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
