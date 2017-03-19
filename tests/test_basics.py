import unittest
from flask import current_app
from app import create_app


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('myApp')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertTrue(current_app)
        self.assertEqual(current_app.name, 'myApp')

    def test_app_in_testing(self):
        self.assertTrue(current_app.config['TESTING'])
