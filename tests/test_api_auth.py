import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import User
from flask import url_for


class ApiAuthTestCase(unittest.TestCase):
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

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_token_valid_auth(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com', password='hassan')
        user.save()
        header = self.get_api_headers(
            'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.client.get(url_for('api.get_token'), headers=header)
        token = response.get_data('token')
        self.assertTrue(token)
        self.assertEqual(response.status_code, 200)

    def test_get_token_invalid_auth(self):
        header = self.get_api_headers('abdulmeen.olasode@andela.com', 'hassan')
        response = self.client.get(url_for('api.get_token'), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        self.assertEqual(response.status_code, 401)

    def test_get_token_no_auth(self):
        header = self.get_api_headers('', '')
        response = self.client.get(url_for('api.get_token'), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Supply a username and password')
        self.assertEqual(response.status_code, 403)

    def test_register_user(self):
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'User creation successful')
        self.assertEqual(response.status_code, 201)

    def test_register_missing_fields(self):
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': '', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('This field is required.', message)
        self.assertEqual(response.status_code, 403)

    def test_register_invalid_email(self):
        user_data = {'email': 'meandela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('Invalid email address.', message)
        self.assertEqual(response.status_code, 403)

    def test_register_not_matching_password(self):
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prak',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('Password must match', message)
        self.assertEqual(response.status_code, 403)

    def test_register_with_existing_email(self):
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('Email already exist', message)
        self.assertEqual(response.status_code, 403)
