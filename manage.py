#!/usr/bin/env python
import os

import dotenv
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import LongUrl, ShortUrl, User, Visitor, visits
dotenv.load()


app = create_app(dotenv.get('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    """
    This function makes the model, database and app available in the shell
    context
    """
    return dict(app=app, db=db, User=User, ShortUrl=ShortUrl,
                LongUrl=LongUrl, visits=visits, Visitor=Visitor)


@manager.command
def test(coverages=False, verbosity=1):
    """
    This function runs nosetests when the manage.py test is called
    giving the option of running with coverage and setting verbosity.
    """
    os.system('nosetests {} --cover-package=app '
              '--verbosity={}'.format(('--with-coverage' * coverages),
                                      verbosity))


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
