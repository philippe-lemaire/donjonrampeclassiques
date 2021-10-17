import os
import sys
import click
from app import create_app, db
from app.models import Role, Character, User
from flask_migrate import upgrade


from flask_migrate import Migrate

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

current_config = os.getenv("FLASK_CONFIG") or "default"

app = create_app(current_config)

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Character=Character)


@app.cli.command()
@click.option(
    "--coverage/--no-coverage", default=False, help="Run tests under code coverage."
)
def test(coverage):
    """Run the unit tests"""
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print(f"HTML version: file://{covdir}/index.html")
        COV.erase()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    # Role.insert_roles()
