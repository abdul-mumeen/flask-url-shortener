import unittest
from flask import current_app
from app import create_app


class BasicsTestCase(unittest.TestCase):
    def create_test_app(self, environ='testing'):
        app = create_app(environ)
        app_context = app.app_context()
        app_context.push()
        return app_context

    def test_app_exists(self):
        app_context = self.create_test_app('testing')
        self.assertTrue(current_app)
        self.assertEqual(current_app.name, 'app')
        app_context.pop()

    def test_app_in_testing(self):
        app_context = self.create_test_app('testing')
        self.assertTrue(current_app.config['TESTING'])
        app_context.pop()

    def test_app_in_dev(self):
        app_context = self.create_test_app('development')
        self.assertTrue(current_app.config['DEBUG'])
        app_context.pop()

    def test_app_in_prod(self):
        app_context = self.create_test_app('production')
        self.assertFalse(current_app.config['DEBUG'])
        app_context.pop()
