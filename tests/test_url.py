import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import LongUrl, ShortUrl, User, Visitor
from flask import current_app, url_for


class UrlTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

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

    def register_user(self, f_name, l_name, email, password):
        user = User(first_name=f_name, last_name=l_name,
                    email=email, password=password)
        user.save()

    def get_token(self, email, password):
        header = self.get_username_headers(email, password)
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

    def user_shorten_url(self, url, vanity, email, password):
        data = json.dumps({'long_url': url, 'vanity': vanity})
        headers = self.get_token_headers(self.get_token(email, password))
        response = self.client.post(url_for('api.shorten'),
                                    data=data, headers=headers)
        return json.loads(response.data)

    def test_anonymous_shorten_same_url(self):
        short_url = self.anonymous_shorten_url('https://www.google.com', '')
        short_url_2 = self.anonymous_shorten_url('https://www.google.com', '')
        self.assertEqual(short_url_2['message'], short_url['message'])

    def test_reg_user_shorten_url(self):
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        success = response['success']
        short_url = response['message']
        self.assertTrue(short_url)
        self.assertIn('http://www.fus.ly/', short_url)
        self.assertTrue(success)

    def test_reg_user_shorten_same_url(self):
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['message']
        response = self.user_shorten_url('https://www.google.com', '',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_2 = response['message']
        self.assertEqual(short_url_1, short_url_2)

    def test_reg_user_shorten_vanity_url(self):
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', 'goo',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        short_url = response['message']
        self.assertEqual(short_url, 'http://www.fus.ly/goo')

    def test_reg_user_shorten_same_vanity_url(self):
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', 'goo',
                                         'abdulmumeen.olasode@andela.com',
                                         'hassan')
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', 'goo',
                                         'angular@node.com', 'python')
        self.assertEqual(response['message'],
                         "Vanity string 'goo' has been taken")

    def test_update_long_url(self):
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['message']
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
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
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['message']
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_2 = response['message']
        response = self.client.get(url_for('api.most_recent'))
        message = json.loads(response.data)['message']
        self.assertEqual(message[0]['short_url'], short_url_2)
        self.assertEqual(message[1]['short_url'], short_url_1)

    def test_deactivate_url(self):
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_url = response['short_url_url']
        response = self.client.put(short_url_url + '/deactivate/')
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.put(
            short_url_url + '/deactivate/', headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, short_url_url)
        self.assertIs(response.status_code, 200)
        # Include testing response when deactivated url is called

    def test_activate_url(self):
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_url = response['short_url_url']
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        headers = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.put(short_url_url + '/activate/')
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.put(
            short_url_url + '/activate/', headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, short_url_url)
        self.assertIs(response.status_code, 200)
        # Include testing response when deactivated url is called
