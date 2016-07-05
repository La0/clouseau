from backend.models import BugAnalysis, BugResult
from backend import db
from clouseau.bugzilla import Bugzilla
from clouseau.patchanalysis import bug_analysis
from sqlalchemy.orm.exc import NoResultFound
import logging
import json

logger = logging.getLogger(__name__)


class AnalysisWorkflow(object):
    """
    Update all analysis data
    """
    def __init__(self):
        self.bugs = {}

    def run(self):
        """
        Main workflow enty point
        """

        all_analysis = BugAnalysis.query.all()
        for analysis in all_analysis:

            # Get bugs from bugzilla, for all analysis
            raw_bugs = self.list_bugs(analysis)

            # Do patch analysis on bugs
            bugs = [self.update_bug(b) for b in raw_bugs.values()]

            # Update sqlalchemy relation
            analysis.bugs[:] = bugs
            db.session.commit()

    def list_bugs(self, analysis):
        """
        List all the bugs in an analysis
        """
        assert isinstance(analysis, BugAnalysis)
        assert analysis.parameters is not None

        logger.info('List bugs for {}'.format(analysis))

        def _bughandler(bug, data):
            data[bug['id']] = bug

        bugs = {}
        bz = Bugzilla(analysis.parameters, bughandler=_bughandler, bugdata=bugs)
        bz.get_data().wait()

        return bugs

    def update_bug(self, bug):
        """
        Update a bug
        """
        # Skip when it's already processed in instance
        bug_id = bug['id']
        if bug_id in self.bugs:
            logger.warn('Bug {} already processed.'.format(bug_id))
            return self.bugs[bug_id]

        # Fetch or create existing bug result
        try:
            br = BugResult.query.filter_by(bugzilla_id=bug_id).one()
            logger.info('Update existing {}'.format(br))
        except NoResultFound:
            br = BugResult(bug_id)
            logger.info('Create new {}'.format(br))

        # Do patch analysis
        try:
            analysis = bug_analysis(bug_id)
        except Exception as e:
            logger.error('Patch analysis failed on {} : {}'.format(bug_id, e))
            return

        payload = {
            'bug': bug,
            'analysis': analysis,
        }
        payload_json = json.dumps(payload)

        # Check payload changed
        # TODO

        # Save payload
        br.payload = payload_json
        db.session.add(br)
        logger.info('Updated payload of {}'.format(br))

        # Save in local cache
        self.bugs[bug_id] = br

        return br
