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
        return json.loads(response.data)['token']

    def test_anonymous_shorten_url(self):
        response = self.anonymous_shorten_url('https://www.google.com', '')
        short_url = response['message']
        success = response['success']
        self.assertTrue(short_url)
        self.assertIn('http://www.fus.ly/', short_url)
        self.assertTrue(success)

    def test_anonymous_shorten_vanity_url(self):
        response = self.anonymous_shorten_url('https://www.google.com', 'go')
        self.assertEqual(response['message'], 'Invalid credentials')
        self.assertEqual(response['error'], 'unauthorized')

    def anonymous_shorten_url(self, url, vanity):
        data = json.dumps({'long_url': url,
                           'vanity': vanity})
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(url_for('api.shorten'),
                                    data=data, headers=headers)
        return json.loads(response.data)

    def user_shorten_url(self, url, vanity):
        data = json.dumps({'long_url': url, 'vanity': vanity})
        response = self.client.post(url_for('api.shorten'),
                                    data=data, headers=self.headers)
        return json.loads(response.data)

    def test_anonymous_shorten_same_url(self):
        short_url = self.anonymous_shorten_url('https://www.google.com', '')
        short_url_2 = self.anonymous_shorten_url('https://www.google.com', '')
        self.assertEqual(short_url_2['message'], short_url['message'])

    def test_reg_user_shorten_url(self):
        response = self.user_shorten_url('https://www.google.com', '')
        success = response['success']
        short_url = response['message']
        self.assertTrue(short_url)
        self.assertIn('http://www.fus.ly/', short_url)
        self.assertTrue(success)

    def test_reg_user_shorten_same_url(self):
        response = self.user_shorten_url('https://www.google.com', '')
        short_url_1 = response['message']
        response = self.user_shorten_url('https://www.google.com', '')
        short_url_2 = response['message']
        self.assertEqual(short_url_1, short_url_2)

    def test_reg_user_shorten_vanity_url(self):
        response = self.user_shorten_url('https://www.google.com', 'goo')
        short_url = response['message']
        self.assertEqual(short_url, 'http://www.fus.ly/goo')

    def test_update_long_url(self):
        response = self.user_shorten_url('https://www.google.com', '')
        short_url_1 = response['message']
        response = self.anonymous_shorten_url('https://www.google.com', '')
        short_url_2 = response['message']
        self.assertNotEqual(short_url_1, short_url_2)
        count = len(LongUrl.query.filter_by(
            long_url='https://www.google.com').all())
        self.assertEqual(count, 1)

    def test_most_recent_urls(self):
        response = self.client.get(url_for('api.most_recent'))
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'No url found')
        self.assertEqual(response.status_code, 404)
        response = self.user_shorten_url('https://www.google.com', '')
        short_url_1 = response['message']
        response = self.anonymous_shorten_url('https://www.google.com', '')
        short_url_2 = response['message']
        response = self.client.get(url_for('api.most_recent'))
        message = json.loads(response.data)['message']
        self.assertEqual(message[0]['short_url'], short_url_2)
        self.assertEqual(message[1]['short_url'], short_url_1)
