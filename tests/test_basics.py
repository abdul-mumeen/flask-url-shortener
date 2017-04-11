import unittest

from app import create_app
from flask import current_app


class BasicsTestCase(unittest.TestCase):
    def create_test_app(self, environ='testing'):
        """
        This function is used to create an instance of the with the selected
        configuration.

        keyword arguments:
        environ -- it is a string value that depict the environment the app
        is running in.
        """
        app = create_app(environ)
        app_context = app.app_context()
        app_context.push()
        return app_context

    def test_app_exists(self):
        """
        This function tests if the application has been created successfully
        after the create app has been invoked,
        """
        app_context = self.create_test_app('testing')
        self.assertTrue(current_app)
        self.assertEqual(current_app.name, 'app')
        app_context.pop()

    def test_app_in_testing(self):
        """
        This function runs to confirm that the application loads the
        testing configuration when testing is selected.
        """
        app_context = self.create_test_app('testing')
        self.assertTrue(current_app.config['TESTING'])
        app_context.pop()

    def test_app_in_dev(self):
        """
        This function runs to confirm that the application loads the
        development configuration when development is selected.
        """
        app_context = self.create_test_app('development')
        self.assertTrue(current_app.config['DEBUG'])
        app_context.pop()

    def test_app_in_prod(self):
        """
        This function runs to confirm that the application loads the
        production configuration when production is selected.
        """
        app_context = self.create_test_app('production')
        self.assertFalse(current_app.config['DEBUG'])
        app_context.pop()
