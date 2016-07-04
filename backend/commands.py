import click
from backend import app, db


@app.cli.command()
def initdb():
    """
    Initialize the database.
    """
    click.echo('Init the db')
    db.create_all()

    # From https://github.com/mozilla/relman-auto-nag/blob/master/auto_nag/scripts/rm_query_creator.py#L12
    click.echo('Add a demo analysis')
    from backend.models import BugAnalysis
    ba = BugAnalysis('demo')
    release_version = '47' # TODO: use a tool for that
    beta_version = '48'
    aurora_version = '49'
    central_version  = '50'
    ba.parameters = "v4=affected&o5=equals&f1=cf_status_firefox" + central_version + "&o3=equals&v3=affected&o1=equals&j2=OR&resolution=---&resolution=FIXED&f4=cf_status_firefox" + beta_version + "&v5=affected&query_format=advanced&f3=cf_status_firefox" + aurora_version + "&f2=OP&o4=equals&f5=cf_status_firefox" + release_version + "&v1=fixed&f7=CP"

    db.session.add(ba)
    db.session.commit()


@app.cli.command()
def run_workflow():
    """
    Run the bug update workflow
    """
    from backend.workflow import AnalysisWorkflow
    workflow = AnalysisWorkflow()
    workflow.run()

