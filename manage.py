#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell
import unittest
from flask_migrate import MigrateCommand

import dotenv

dotenv.load()

app = create_app(dotenv.get('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    """Make shell context"""
    return dict(app=app, db=db)


@manager.command
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
