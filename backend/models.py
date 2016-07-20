from __future__ import absolute_import
from backend import db
import datetime
import pickle

# M2M link between analysis & bug
bugs = db.Table(
    'analysis_bugs',
    db.Column('analysis_id', db.Integer, db.ForeignKey('bug_analysis.id')),
    db.Column('bug_id', db.Integer, db.ForeignKey('bug_result.id'))
)


class BugAnalysis(db.Model):
    """
    A template to build some cached analysis
    by listing several bugs from Bugzilla, with
    their analysus
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    parameters = db.Column(db.Text())
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    bugs = db.relationship('BugResult', secondary=bugs, backref=db.backref('analysis', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'AnalysisTemplate {}'.format(self.name)


class BugResult(db.Model):
    """
    The cached result of an analysis run
    """
    id = db.Column(db.Integer, primary_key=True)
    bugzilla_id = db.Column(db.Integer, unique=True)
    payload = db.Column(db.Text())
    payload_hash = db.Column(db.String(40))

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, bugzilla_id):
        self.bugzilla_id = bugzilla_id

    def __repr__(self):
        return 'BugResult {}'.format(self.bugzilla_id)

    @property
    def payload_data(self):
        if not self.payload:
            return None
        return pickle.loads(self.payload)
