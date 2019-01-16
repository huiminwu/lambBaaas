import json, urllib, os, sqlite3

from flask import Flask, render_template, flash, request, session, redirect, url_for

from datetime import datetime
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
data.createActivities()

def getText():
    #F = open("data/hamlet.txt","r")
    #text = F.read()
    text = api.get_quote()
    result = text['quote'] + " -" + text['author']
    #flash(result)
    result = result.replace("&#8211;", '-')
    result = result.replace("&#8212;", '-')
    result = result.replace("&#8220;", '"')
    result = result.replace("&#8221;", '"')
    result = result.replace("&#8216;", "'")
    result = result.replace("&#8217;", "'")
    result = result.replace("&#8230;", "...")
    result = result.replace("&#8206;", "")
    result = result.replace("&#8232;", "")
    result = result.replace("&mdash;", "-")
    result = result.replace("&lt;strong&gt;", "")
    result = result.replace("&lt;em&gt;", "")
    result = result.replace("<br />", "")
    result = result.replace("</p>", "")
    result = result.replace("<p>", "")
    return result

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
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
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

    return render_template("homepage.html", loggingin = True)

@app.route('/activity')
def bored_activity():
    '''
    Displays random activity and ones saved for user
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    result = api.get_bored_activity()
    print(result)
    activity = result['activity']
    category = result['type']
    participant = result['participants']
    row = data.getActivities(user) #should recieve dict
    return render_template("activity.html", randact = activity,
                                            randcat = category,
                                            randpart = participant,
                                            diction = row
                                            )

@app.route('/saveAct', methods=['POST'])
def save_act():
    '''
    Saves Activity
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    activity = request.form['act']
    print(activity)
    category = request.form['cat']
    part = request.form['part']
    data.saveAct(user, activity, category, part)
    flash('{} saved!'.format(activity))
    return redirect(url_for('bored_activity'))


@app.route('/newAct', methods=['POST'])
def new_act():
    '''
    Gives user a new activity
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    return redirect(url_for('bored_activity'))

@app.route('/deleteAct', methods=['POST'])
def delete_act():
    '''
    Deletes Activity
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    activity = request.form['act']
    print(activity)
    data.deleteAct(user, activity)
    flash('{} deleted!'.format(activity))
    return redirect(url_for('bored_activity'))

@app.route('/vocab', methods=['POST', 'GET'])
def vocab():
    '''
    Vocab home page.
    Displays all words, and an option to search for words.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    words = data.getVocabWords(user)
    print(words)
    return render_template('vocab.html', user_name = user, loggedin = "True", words = words)


@app.route('/wordSearch')
def word_activity():
    '''
    Displays a search query for words.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    return render_template("word_search.html")

@app.route('/wordResult', defaults={'word': None})
@app.route('/wordResult/<word>')
def search_results(word):
    '''
    Returns all entries for the word.
    Has an optional param for returning from the defintions endpoint.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    if word:
        query = word
    else:
        query = request.args['query']
        # checking for common mistakes
        query = query.strip()
        # check for special chars as well
        if query == '' or any(i in '!@#$%^&*()[]{}\|;\',.<>/\"' for i in query):
            flash('Input something valid!')
            return render_template("word_search.html")

        query = query.replace(' ', '%20')

    result = api.get_word(query)
    if result['words'] == []:
        flash('No suitable words found!')
    return render_template('word_search.html', **result)

@app.route('/def/<word>', defaults={'oldQuery': None})
@app.route('/def/<oldQuery>/<word>')
def definition(oldQuery, word):
    '''
    returns the definition of the selected word. Employs this through dynamic routing.
    if no defintions exist, user is returned to the previous page.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    # placeholder for spaces
    new_word = word.replace(' ','%20')
    new_word = word.replace('+', '%20')
    result = api.get_definition(new_word)

    if result == {}:
        flash('No definitions found!')
        if oldQuery:
            # save oldQuery in the result as well
            return redirect(url_for('search_results', word = oldQuery))
        return redirect(url_for('vocab'))

    # add in fine-tune adjustments to the dict
    result['word'] = word
    print(word, result)
    result['oldQuery'] = oldQuery
    return render_template('definitions.html', **result)

@app.route('/saveWord', methods = ['POST'])
def saveWord():
    '''
    Saves the input word to the DB. POST-only method.
    Redirects back to the vocab route
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    word = request.form['word']
    try:
        data.saveWord(user, word)
    except sqlite3.IntegrityError as e:
        flash('This word is already saved!')
        return redirect(url_for('vocab'));
    flash('Word {} saved!'.format(word))
    return redirect(url_for('vocab'))

@app.route('/deleteWord/<word>')
def deleteWord(word):
    '''
    Deletes the word from the database.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    data.deleteWord(user, word)
    flash('Word deleted!')
    return redirect(url_for('vocab'))

@app.route('/typing', methods=['POST', 'GET'])
def typing():
    '''
    Typing page.
    '''
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
    return render_template('typing.html',
                            user_name = user,
                            loggedin = "True",
                            text = getText())

@app.route('/typingResults', methods=['POST'])
def typingResults():
    '''
    Display results and update database.
    '''
    dif, time, wpm, acc = request.form["dif"],request.form["time"], request.form['wpm'], request.form['accuracy']
    flash(""+ dif + " " + time + " " + wpm + " " + acc)
    if (int(acc)>=95):
        if(not data.isInDB('typing')):
            data.createTyping()
        if(data.getWPM(user,dif)<wpm):
            data.saveWPM(user,wpm,time,dif)
    #datetime.fromtimestamp(int(time)/1000.0)
    return render_template('results.html',
                            user_name = user,
                            loggedin = "True",
                            difficulty = dif,
                            timestamp = time,
                            wpm = wpm,
                            accuracy = acc)

@app.route('/leaderboard')
def leaderboard():
    '''
    Display leaderboard.
    '''
    flash(data.getLeaderboard())
    return render_template('leaderboard.html',
                            user_name = user,
                            loggedin = "True",
                            leaderboard = data.getLeaderboard())

if (__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
