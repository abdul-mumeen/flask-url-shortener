#!/usr/bin/env python
import os
import sys
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
def test(coverages=False, verbosity=1):
    print(coverages, verbosity)
    """Run the unit tests with coverage when set to true."""
    os.system('nosetests {} --cover-package=app '
              '--verbosity={}'.format(('--with-coverage' * coverages), verbosity))


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
