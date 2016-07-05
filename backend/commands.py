import click
from backend import app, db
from clouseau import versions


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

    all_versions = {k: v[:v.index('.')] for k, v in versions.get().items()}  # use major versions
    ba.parameters = "v4=affected&o5=equals&f1=cf_status_firefox{nightly}&o3=equals&v3=affected&o1=equals&j2=OR&resolution=---&resolution=FIXED&f4=cf_status_firefox{beta}&v5=affected&query_format=advanced&f3=cf_status_firefox{aurora}&f2=OP&o4=equals&f5=cf_status_firefox{release}&v1=fixed&f7=CP".format(**all_versions)

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
