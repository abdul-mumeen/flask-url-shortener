import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import User
from flask import url_for


class ApiAuthTestCase(unittest.TestCase):
    def setUp(self):
        """
        This function runs before each test initializing the application and
        creating a client that will consume it.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        """
        This function runs after each test removing the session and destroying
        the table that might have been created during testing.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, email, password):
        """
        This function returns a dictionary which contains a request header
        encoded with the email and password authorization details.
        """
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_token_valid_auth(self):
        """
        This function tests the response from getting a token using a valid
        email and password
        """
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
        """
        This function tests the response from getting a token using an invalid
        email and password
        """
        header = self.get_api_headers('abdulmeen.olasode@andela.com', 'hassan')
        response = self.client.get(url_for('api.get_token'), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        self.assertEqual(response.status_code, 401)

    def test_get_token_no_auth(self):
        """
        This function tests the response from getting a token using with no
        email and password.
        """
        header = self.get_api_headers('', '')
        response = self.client.get(url_for('api.get_token'), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Supply a username and password')
        self.assertEqual(response.status_code, 403)

    def test_register_user(self):
        """
        This function tests the response from registering a user with
        complete and valid user information.
        """
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
        """
        This function tests the response from registering a user with
        missing user information.
        """
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': '', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('All entities first_name, last_name, email, password,'
                      ' confirm_password are required', message)
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_email(self):
        """
        This function tests the response from registering a user with
        complete but invalid email address.
        """
        user_data = {'email': 'meandela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prank',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('Invalid email address.', message)
        self.assertEqual(response.status_code, 400)

    def test_register_not_matching_password(self):
        """
        This function tests the response from registering a user with
        complete but not matching passwords.
        """
        user_data = {'email': 'me@andela.com', 'first_name': 'Adedoyin',
                     'last_name': 'Fujitsu', 'password': 'prak',
                     'confirm_password': 'prank'
                     }
        header = {'Content-Type': 'application/json'}

        response = self.client.post(url_for('api.register_user'),
                                    data=json.dumps(user_data), headers=header)
        message = json.loads(response.data)['message']
        self.assertIn('Password must match', message)
        self.assertEqual(response.status_code, 400)

    def test_register_with_existing_email(self):
        """
        This function tests the response from registering a user with
        existing email address.
        """
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
