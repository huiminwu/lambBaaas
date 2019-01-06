import os
from time import strftime

from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify

from utils import api, db
from random import choice

app = Flask(__name__) #create instance of class Flask

@app.route('/')
def index():
    return 'Hello world!'


if __name__ == '__main__':
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
