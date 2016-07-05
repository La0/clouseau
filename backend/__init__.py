from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Setup app
app = Flask('clouseau_backend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # warning
db = SQLAlchemy(app)

# Expose commands, api & models
from backend.commands import initdb
from backend.models import BugAnalysis, BugResult
from backend import api

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Routing
app.add_url_rule('/', view_func=api.home)
app.add_url_rule('/analysis/<analysis_id>/', view_func=api.analysis)
