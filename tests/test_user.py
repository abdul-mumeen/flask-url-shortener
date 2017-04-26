import json
import unittest

from flask import url_for

from util import UserDetailHelper as user_helper


class UrlTestCase(unittest.TestCase):
    def setUp(self):
        """
        This function runs before each test initializing the application
        creating tables in the db and creating a client that will consume it.
        """
        self.uh = user_helper()
        self.uh.set_up()

    def tearDown(self):
        """
        This function runs after each test removing the session and destroying
        the table that might have been created during testing.
        """
        self.uh.tear_down()

    def test_get_empty_influential_users(self):
        response = self.uh.client.get(url_for('api.influential'))
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 404)
        self.assertEqual(message, 'No user found')

    def test_get_infuential_users(self):
        self.uh.register_user('Mumeen', 'Olasode', 'olasode@andela.com', 'and')
        response = self.uh.user_shorten_url(
            'https://www.google.com', '', 'olasode@andela.com', 'and')
        user_1_url_1 = response['url']['short_url']
        response = self.uh.user_shorten_url(
            'https://www.facebook.com', '', 'olasode@andela.com', 'and')
        user_1_url_2 = response['url']['short_url']
        self.uh.register_user('Ladi', 'Adeniran', 'ladi@andela.com', 'yeah')
        response = self.uh.user_shorten_url(
            'https://www.stackoverflow.com', '', 'ladi@andela.com', 'yeah')
        user_2_url_1 = response['url']['short_url']

        headers = {'Content-Type': 'application/json'}
        data_1 = json.dumps({'short_url': user_1_url_1})
        self.uh.client.post(url_for('api.visit'), data=data_1, headers=headers)

        data_2 = json.dumps({'short_url': user_1_url_2})
        self.uh.client.post(url_for('api.visit'), data=data_2, headers=headers)

        data_3 = json.dumps({'short_url': user_2_url_1})
        self.uh.client.post(url_for('api.visit'), data=data_3, headers=headers)
        self.uh.client.post(url_for('api.visit'), data=data_3, headers=headers)
        self.uh.client.post(url_for('api.visit'), data=data_3, headers=headers)

        response = self.uh.client.get(
            url_for('api.influential'), headers=headers)
        users = json.loads(response.data)['users']
        self.assertIsNotNone(users)
        self.assertEqual(users[0]['first_name'], 'Ladi')
        self.assertEqual(users[0]['number_of_visits'], 3)
        self.assertEqual(users[1]['first_name'], 'Mumeen')
        self.assertEqual(users[1]['number_of_visits'], 2)

    def test_get_user_details(self):
        self.uh.register_user('Mumeen', 'Olasode', 'olasode@andela.com', 'and')
        headers = self.uh.get_token_headers(
            self.uh.get_token('olasode@andela.com', 'and'))
        response = self.uh.client.get(url_for('api.user'), headers=headers)
        user = json.loads(response.data)['user']
        self.assertEqual(user['first_name'], 'Mumeen')
        self.assertEqual(user['last_name'], 'Olasode')
        self.assertFalse(user['short_urls'])

    def test_user_route_with_no_credentials(self):
        response = self.uh.client.get(url_for('api.user'))
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        self.assertEqual(response.status_code, 401)
