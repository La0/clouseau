from backend.models import BugAnalysis
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify, abort


def home():
    return 'Clouseau API'

def _serialize_analysis(analysis):
    """
    Helper to serialize an analysis
    """
    return {
        'id': analysis.id,
        'name': analysis.name,
        'bugs': [{
            'id': b.id,
            'bugzilla_id': b.bugzilla_id,
            'payload': b.payload_data,
        } for b in analysis.bugs if b.payload],
    }

def analysis_list():
    """
    List all available analysis
    """
    all_analysis = BugAnalysis.query.all()
    return jsonify([_serialize_analysis(analysis) for analysis in all_analysis])

def analysis_details(analysis_id):
    """
    Fetch an analysis and all its bugs
    """

    # Get bug analysis
    try:
        analysis = BugAnalysis.query.filter_by(id=analysis_id).one()
    except NoResultFound:
        abort(404)

    # Build JSON output
    return jsonify(_serialize_analysis(analysis))
