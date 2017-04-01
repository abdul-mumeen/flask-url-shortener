#!/usr/bin/env python
import os
import unittest

import coverage
import dotenv
from app import create_app, db
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

dotenv.load()

app = create_app(dotenv.get('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    """Make shell context"""
    return dict(app=app, db=db)


@manager.command
def test(coverage_check=False):
    """Run the unit tests with coverage when set to true."""
    coverall = None
    if coverage_check:
        coverall = coverage.coverage(
            branch=True, include='app/*')
        coverall.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if coverall:
        coverall.stop()
        coverall.save()
        print('Coverage Summary:')
        coverall.report(show_missing=True)
        coverall.erase()


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
