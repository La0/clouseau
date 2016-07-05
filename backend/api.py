from backend.models import BugAnalysis
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify, abort


def home():
    return 'Clouseau API'


def analysis(analysis_id):
    """
    Fetch an analysis and all its bugs
    """

    # Get bug analysis
    try:
        analysis = BugAnalysis.query.filter_by(id=analysis_id).one()
    except NoResultFound:
        abort(404)

    # Build JSON output
    out = {
        'id': analysis.id,
        'name': analysis.name,
        'bugs': [{
            'id': b.id,
            'bugzilla_id': b.bugzilla_id,
            'payload': b.payload_data,
        } for b in analysis.bugs],
    }
    return jsonify(out)
