from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setup app
app = Flask('clouseau_backend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # warning
db = SQLAlchemy(app)

# Expose commands, models, views
from backend.commands import initdb
from backend.models import *


@app.route('/')
def hello_world():
    return 'Hello, World!'
