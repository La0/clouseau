from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_cors import CORS


# Setup app
app = Flask('clouseau_backend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # warning
db = SQLAlchemy(app)

# Enable CORS requests
CORS(app)

# Expose commands, api & models
from backend.commands import initdb
from backend.models import BugAnalysis, BugResult
from backend.serializers import TimedeltaJSONEncoder
from backend import api

# Use our default serializer
app.json_encoder = TimedeltaJSONEncoder


# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Routing
app.add_url_rule('/', view_func=api.home)
app.add_url_rule('/analysis/<analysis_id>/', view_func=api.analysis)
