from backend.models import BugAnalysis
from clouseau.bugzilla import Bugzilla, BugResult
from sqlalchemy.orm.exc import NoResultFound
import logging

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

        # Get bugs from bugzilla, for all analysis
        all_analysis = BugAnalysis.query.all()
        for analysis in all_analysis:
            self.bugs.update(self.list_bugs(analysis))

        # Do patch analysis on bugs
        for bug_id, bug in self.bugs.items():
            self.update_bug(bug)


    def list_bugs(self, analysis):
        """
        List all the bugs in an analysis
        """
        assert isinstance(analysis, BugAnalysis)
        assert analysis.parameters is not None

        logger.info('List bugs for analysis {}'.format(analysis))

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
        # Fetch or create existing bug result
        bug_id = bug['id']
        try:
            result = BugResult.query.filter(bugzilla=bug_id).one()
            logger.info('Update existing {}'.format(result))
        except NoResultFound:
            result = BugResult(bug_id)
            logger.info('Create new {}'.format(result))

        # Do patch analysis
        # TODO

        # Update result payload if modified


