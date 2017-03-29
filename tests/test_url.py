import unittest
from app import create_app, db
from flask import current_app, url_for
from app.models import ShortUrl, LongUrl, User, Visitor
from base64 import b64encode
import json


class UrlTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        self.headers = self.get_token_headers(self.get_token())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_username_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_token_headers(self, token):
        return {
            'Authorization': 'Token ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com', password='hassan')
        user.save()
        header = self.get_username_headers('abdulmumeen.olasode@andela.com', 'hassan')
        response = self.client.get(url_for('api.get_token'), headers=header)
        return response.get_data('token')

    def test_anonymous_shorten_url(self):
        data = {'long_url': 'https://www.google.com'}
        response = self.client.get(url_for('api.shorten'),
                                   headers=self.headers, data=data)
        short_url = response.get_data('message')
        success = response.get_data('success')
        self.assertTrue(short_url)
        self.assertIn('http://www.fus.ly/', message)
        self.assertTrue(success)
