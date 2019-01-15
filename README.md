# Team: lambBaaas
## Members: Hui Min Wu (PM), Raunak Chowdhury, and Anton Danylenko
## Project Name: Git Güd
---
### Brief Overview

This website allows someone to take advantage of the new year to git güd — that is, to expand one’s vocabulary and improve their (touch) typing speed. If they’ve mastered all that, they can git güder by checking out random activities we have on our site and getting more involved in the world around them.

---
### Dependencies
- Virtual environment: helps manage the libraries used in this project without affecting your other projects
- Python 3: The language in which our python files are coded in
- Flask: a web framework for Python web applications
- Werkzeug: installed automatically when installing Flask. Implements WSGI the standard Python interface between apps and servers
- Jinja: installed automatically when installing Flask. A template language that renders pages your app serves
- ItsDangerous: installed automatically when installing Flask. Securely signs data to ensure its integrity.
- Click: installed automatically when installing Flask. Framework for writing command line applications.

---
### How to Run
1. This project requires python3 so run `python3` in your terminal and you should be prompted this:
```
Python 3.6.5 (default, Apr 1 2018, 05:46:30)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
If not, install python3.6 by typing `sudo apt-get install python3.6`

2. Activate your virtual environment by typing `$ . PATH_TO_VENV/VENV/bin/activate` in terminal. If you haven't procured a virtual environment before, install python3-venv and create your own by pasting the following below in your terminal:
```
sudo apt install python3-venv
python3 -m venv <VENV_NAME>
```
3. Procure and upload api keys
4. Install necessary plugins with : `pip install -r <path-to-file>requirements.txt` in your venv
5. Clone this repo either by:
HTTPS: `https://github.com/huiminwu/lambBaaas.git`
SSH: `git@github.com:huiminwu/lambBaaas.git`

6. Change to `lambBaaas/` on your machine and type `python app.py` in your terminal. This should return with a link to our application, running on your localhost.

---
### API keys

API | Description
------------ | -------------
Oxford | Lists all definitions of a word if there are definitions available
Datamuse | Lists all possible words related to the string query requested.
QuotesOnDesign | Returns a random quote and the author of that quote.
Bored | Returns a random activity to do when you're bored.

#### Oxford API
1. Select the free plan at https://developer.oxforddictionaries.com/?tag=#plans.
1. Fill out information and you should recieve the API key.
1. Place API key in `<reporoot>/keys/oxford.txt`

#### Datamuse API
None requried!
#### QuotesOnDesign API
None requried!
#### Bored API
None requried!

---
<p align="center"> <img src="https://github.com/huiminwu/lambBaaas/blob/master/static/logo.png"></p>
