import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import LongUrl, User
from flask import url_for


class UrlTestCase(unittest.TestCase):
    def setUp(self):
        """
        This function runs before each test initializing the application
        creating tables in the db and creating a client that will consume it.
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

    def get_username_headers(self, email, password):
        """
        This function returns a dictionary which contains a request header
        encoded with the email and password authorization details.

        keyword arguments:
        email -- a string holding the user email address
        passsword -- a string holding the user password
        """
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_token_headers(self, token):
        """
        This function returns a dictionary which contains a request header
        encoded with the users token for authorization.

        keyword argument:
        token -- a string containing randomly generated encoded characters
        """
        return {
            'Authorization': 'Token ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def register_user(self, f_name, l_name, email, password):
        """
        This function registers a user with the user information supplied

        keyword arguments:
        f_name -- a string containing the user's firt name
        l_name -- a string containing the user's last name
        email -- a string holding the user email address
        passsword -- a string holding the user password
        """
        user = User(first_name=f_name, last_name=l_name,
                    email=email, password=password)
        user.save()

    def get_token(self, email, password):
        """
        This function returns a token using the user's email and password.

        keyword arguments:
        email -- a string holding the user email address
        passsword -- a string holding the user password
        """
        header = self.get_username_headers(email, password)
        response = self.client.get(url_for('api.get_token'), headers=header)
        return json.loads(response.data)['token']

    def test_anonymous_shorten_url(self):
        """
        This function tests the response when an anonymous user shorten URL
        """
        response = self.anonymous_shorten_url('https://www.google.com', '')
        short_url = response['url']
        success = response['success']
        self.assertTrue(short_url['short_url'])
        self.assertIn('http://www.fus.ly/', short_url['short_url'])
        self.assertTrue(success)
        response = self.anonymous_shorten_url('https://www.facebook.com', '')
        self.assertTrue(response['success'])

    def test_anonymous_shorten_vanity_url(self):
        """
        This function tests the response when an anonymous user shorten URL
        using vanity string.
        """
        response = self.anonymous_shorten_url('https://www.google.com', 'go')
        self.assertEqual(response['message'], 'Invalid credentials')
        self.assertEqual(response['error'], 'unauthorized')

    def anonymous_shorten_url(self, url, vanity):
        """
        This function shortens URL with anonymous access.

        keyword arguments:
        url -- a string containing the long URL to be shortened.
        vanity -- a string representing the vanity string to be used.
        """
        data = json.dumps({'long_url': url,
                           'vanity': vanity})
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(url_for('api.shorten'),
                                    data=data, headers=headers)
        return json.loads(response.data)

    def user_shorten_url(self, url, vanity, email, password):
        """
        This function shortens URL with registered user access.

        keyword arguments:
        url -- a string containing the long URL to be shortened.
        vanity -- a string representing the vanity string to be used.
        email -- a string containing the email address of the user.
        password -- a string containing the password of the user
        """
        data = json.dumps({'long_url': url, 'vanity': vanity})
        headers = self.get_token_headers(self.get_token(email, password))
        response = self.client.post(url_for('api.shorten'),
                                    data=data, headers=headers)
        return json.loads(response.data)

    def test_anonymous_shorten_same_url(self):
        """
        This function tests the response when an anonymous user shortened
        URL previous shortened by another anonymous user.
        """
        url = self.anonymous_shorten_url('https://www.google.com', '')
        url_2 = self.anonymous_shorten_url('https://www.google.com', '')
        self.assertEqual(url_2['url']['short_url'], url['url']['short_url'])

    def test_reg_user_shorten_url(self):
        """
        This function tests the response when a registered user shorten URL.
        """
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            'https://www.google.com', '',
            'abdulmumeen.olasode@andela.com', 'hassan')
        success = response['success']
        url = response['url']
        self.assertTrue(url['short_url'])
        self.assertIn('http://www.fus.ly/', url['short_url'])
        self.assertTrue(success)

    def test_shorten_empty_url(self):
        """
        This function tests the warning message when a registered user tries
        to shorten an empty URL.
        """
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            '', '', 'abdulmumeen.olasode@andela.com', 'hassan')
        self.assertIn('This field is required.', response['message'])

    def test_reg_user_shorten_same_url(self):
        """
        This function tests the response when registered users tries
        to shorten a URL they have shortened before.
        """
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            'https://www.google.com', '',
            'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['url']['short_url']
        response = self.user_shorten_url(
            'https://www.google.com', '',
            'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_2 = response['url']['short_url']
        self.assertEqual(short_url_1, short_url_2)

    def test_reg_user_shorten_vanity_url(self):
        """
        This function tests a registered user shortens a URL using a prefered
        vanity string.
        """
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            'https://www.google.com', 'goo',
            'abdulmumeen.olasode@andela.com', 'hassan')
        short_url = response['url']['short_url']
        self.assertEqual(short_url, 'http://www.fus.ly/goo')

    def test_reg_user_shorten_same_vanity_url(self):
        """
        This function tests a registered user shortens a URL using a prefered
        vanity string that has been taken.
        """
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
        response = self.user_shorten_url('https://www.google.com', 'goo',
                                         'abdulmumeen.olasode@andela.com',
                                         'hassan')
        self.assertEqual(response['info'], 'Url shortened by you before')

    def test_update_long_url(self):
        """
        This function tests that the long URL is updated when a URL is
        shortened.
        """
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            'https://www.google.com', '',
            'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['url']['short_url']
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_2 = response['url']['short_url']
        self.assertNotEqual(short_url_1, short_url_2)
        count = len(LongUrl.query.filter_by(
            long_url='https://www.google.com').all())
        self.assertEqual(count, 1)

    def test_most_recent_urls(self):
        """
        This function tests the result of querying for the most recent
        shortened URLs.
        """
        response = self.client.get(url_for('api.most_recent'))
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'No url found')
        self.assertEqual(response.status_code, 404)
        self.register_user('Abdul-Mumeen', 'Olasode',
                           'abdulmumeen.olasode@andela.com', 'hassan')
        response = self.user_shorten_url(
            'https://www.google.com', '',
            'abdulmumeen.olasode@andela.com', 'hassan')
        short_url_1 = response['url']['short_url']
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_2 = response['url']['short_url']
        response = self.client.get(url_for('api.most_recent'))
        message = json.loads(response.data)['recents']
        self.assertEqual(message[0]['short_url'], short_url_2)
        self.assertEqual(message[1]['short_url'], short_url_1)

    def test_deactivate_url(self):
        """
        This function tests deactivating a short URL.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        url_response = self.user_shorten_url('https://www.google.com', '',
                                             'angular@node.com', 'python')
        short_url_url = url_response['url']['short_url_url']
        response = self.client.put(short_url_url + '/deactivate')
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.put(
            short_url_url + '/deactivate', headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, short_url_url)
        self.assertIs(response.status_code, 200)
        data = json.dumps({'short_url': url_response['url']['short_url']})
        response = self.client.post(
            url_for('api.visit'),
            data=data, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(response.data)['message'],
                         'URL has been deactivated')

    def test_activate_url(self):
        """
        This function tests activating a short URL.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_url = response['url']['short_url_url']
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        headers = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.put(
            short_url_url + '/activate', headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, 'Invalid credentials')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.put(
            short_url_url + '/activate', headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, short_url_url)
        self.assertIs(response.status_code, 200)

    def test_get_url_details(self):
        """
        This function tests the retrieval of the details of a short URL.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        short_url_url = response['url']['short_url_url']
        short_url = response['url']['short_url']
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.get(
            url_for('api.shorturl', id=1), headers=headers)
        url_details = json.loads(response.data)['url']
        self.assertEqual(url_details['short_url_url'], short_url_url)
        self.assertEqual(url_details['short_url'], short_url)
        self.assertEqual(url_details['long_url'], 'https://www.google.com')

    def test_unauthorized_access_of_url(self):
        """
        This function tests security around accessing a short url without the
        appropraite credentials.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        headers = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.get(
            url_for('api.shorturl', id=1), headers=headers)
        self.assertEqual("No shortened url with id '1' found for you",
                         json.loads(response.data)['message'])
        self.assertEqual(response.status_code, 404)

    def test_get_user_urls(self):
        """
        This function tests retrieval a list short URLs shortened by a
        particular user.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        headers = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.get(
            url_for('api.shorturls'), headers=headers)
        self.assertEqual(json.loads(response.data)[
                         'message'], 'No shortened url found')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'flask@django.com', 'numpy')
        response = self.client.get(
            url_for('api.shorturls'), headers=headers)
        self.assertTrue(type(json.loads(response.data)['urls']) == list)
        self.assertEqual(json.loads(response.data)[
                         'urls'][0]['long_url'],
                         'https://www.google.com')

    def test_delete_short_url(self):
        """
        This function tests deleting a short URL.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        response = self.client.get(
            url_for('api.shorturl', id=1), headers=headers)
        url_details = json.loads(response.data)['url']
        self.assertEqual(url_details['long_url'], 'https://www.google.com')
        response = self.client.delete(
            url_for('api.shorturl', id=1), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            url_for('api.shorturl', id=1), headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "No shortened url with id '1' found for you")
        self.assertEqual(response.status_code, 404)
        response = self.client.put(
            url_for('api.activate_url', id=1), headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_short_url_sharing_long_url(self):
        """
        This function tests the deleting of a short URL that is linked a
        long URL being shared by another short URL.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        headers_2 = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.user_shorten_url('https://www.google.com', '',
                                         'flask@django.com', 'numpy')
        response = self.client.delete(
            url_for('api.shorturl', id=1), headers=headers)
        response = self.client.get(
            url_for('api.shorturl', id=2), headers=headers_2)
        url_details = json.loads(response.data)['url']
        self.assertEqual(url_details['long_url'], 'https://www.google.com')

    def test_change_url_target(self):
        """
        This function tests the changing of the long URL targetted by a
        shortened URL for a registered user.
        """
        self.register_user('Angula', 'Node', 'angular@node.com', 'python')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'angular@node.com', 'python')
        headers = self.get_token_headers(
            self.get_token('angular@node.com', 'python'))
        data = json.dumps({'long_url': ''})
        response = self.client.put(
            url_for('api.shorturl', id=1), headers=headers, data=data)
        message = json.loads(response.data)['message']
        self.assertIn('This field is required.', message)
        data = json.dumps({'long_url': 'https://www.facebook.com'})
        response = self.client.put(
            url_for('api.shorturl', id=1), headers=headers, data=data)
        message = json.loads(response.data)['message']
        self.assertEqual('updated', message)
        self.assertEqual(response.status_code, 200)
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        response = self.user_shorten_url('https://www.google.com', '',
                                         'flask@django.com', 'numpy')
        response = self.user_shorten_url('https://www.facebook.com', '',
                                         'flask@django.com', 'numpy')
        data = json.dumps({'long_url': 'https://www.google.com'})
        response = self.client.put(
            url_for('api.shorturl', id=1), headers=headers, data=data)
        message = json.loads(response.data)['message']
        self.assertEqual('updated', message)

    def test_visits_to_empty_url(self):
        """
        This function tests users hitting the visit route without supplying
        a short URL.
        """
        header = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': ''})
        response = self.client.post(
            url_for('api.visit'), headers=header, data=data)
        message = json.loads(response.data)['message']
        self.assertIn('This field is required.', message)

    def test_visits_to_not_existing_url(self):
        """
        This function tests users hitting the visit route with not existing
        short URL.
        """
        header = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': 'http://www.fus.ly/jLedO'})
        response = self.client.post(
            url_for('api.visit'), headers=header, data=data)
        message = json.loads(response.data)['message']
        self.assertEqual('No matching URL found', message)

    def test_visits_to_deactivated_url(self):
        """
        This function tests users hitting the visit route with a deactivated
        short URL.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        url_response = self.user_shorten_url('https://www.google.com', '',
                                             'flask@django.com', 'numpy')
        headers = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.put(
            url_for('api.deactivate_url', id=1), headers=headers)
        header = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': url_response['url']['short_url']})
        response = self.client.post(
            url_for('api.visit'), headers=header, data=data)
        message = json.loads(response.data)['message']
        self.assertEqual('URL has been deactivated', message)

    def test_visits_to_url(self):
        """
        This function tests users hitting the visit route with a valid
        short URL.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        url_response = self.user_shorten_url('https://www.google.com', '',
                                             'flask@django.com', 'numpy')
        header = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': url_response['url']['short_url']})
        response = self.client.post(
            url_for('api.visit'), headers=header, data=data)
        message = json.loads(response.data)['long_url']
        self.assertEqual('https://www.google.com', message)

    def test_get_visitor_with_invalid_id(self):
        """
        This function tests getting visitor's details with invalid visitor
        id.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        header = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.get(
            url_for('api.visitor', id=1, vid=1), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "No URL found with id '1'")
        self.user_shorten_url('https://www.facebook.com', '',
                              'flask@django.com', 'numpy')
        response = self.client.get(
            url_for('api.visitor', id=1, vid=1), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "No visitor to this URL with id '1'")

    def test_get_visitor_details(self):
        """
        This function tests getting visitor's details with valid visitor
        id.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        header = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        url_response = self.user_shorten_url('https://www.facebook.com', '',
                                             'flask@django.com', 'numpy')

        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': url_response['url']['short_url']})
        response = self.client.post(
            url_for('api.visit'), headers=headers, data=data,
            environ_base={'HTTP_USER_AGENT': 'Chrome, windows',
                          'REMOTE_ADDR': '127.0.0.1'})

        response = self.client.get(
            url_for('api.visitor', id=1, vid=1), headers=header)
        visitor = json.loads(response.data)['visitor']
        self.assertIsInstance(visitor, dict)
        self.assertIsNotNone(visitor['ip_address'])
        self.assertEqual(visitor['browser'], 'chrome')
        self.assertEqual(visitor['platform'], 'windows')
        self.assertIsNotNone(visitor['short_urls'])

    def test_get_visitors_with_invalid_short_url_id(self):
        """
        This function tests getting a list of visitors to a particular URL
        with an invalid URL id.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        header = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        response = self.client.get(
            url_for('api.visitors', id=1), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "No URL found with id '1'")
        self.user_shorten_url('https://www.facebook.com', '',
                              'flask@django.com', 'numpy')
        response = self.client.get(
            url_for('api.visitors', id=1), headers=header)
        message = json.loads(response.data)['message']
        self.assertEqual(message, "No visitor found for this URL")

    def test_get_visitors_details(self):
        """
        This function tests getting a list of visitors (and their details) to
        a particular URL with a valid URL id.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        header = self.get_token_headers(
            self.get_token('flask@django.com', 'numpy'))
        url_response = self.user_shorten_url('https://www.facebook.com', '',
                                             'flask@django.com', 'numpy')

        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': url_response['url']['short_url']})
        response = self.client.post(
            url_for('api.visit'), headers=headers, data=data,
            environ_base={'HTTP_USER_AGENT': 'Chrome, windows',
                          'REMOTE_ADDR': '127.0.0.1'})

        response = self.client.get(
            url_for('api.visitors', id=1), headers=header)

        visitors = json.loads(response.data)['visitors']
        self.assertIsInstance(visitors, list)
        self.assertIsInstance(visitors[0], dict)
        self.assertIsNotNone(visitors[0]['ip_address'])
        self.assertIsNotNone(visitors[0]['browser'])
        self.assertIsNotNone(visitors[0]['platform'])
        self.assertIsNotNone(visitors[0]['short_urls'])

    def test_popular_url(self):
        """
        This function tests getting a list of popular URLs based on the total
        number of visits to the URL.
        """
        self.register_user('flask', 'django', 'flask@django.com', 'numpy')
        url_1_response = self.user_shorten_url('https://www.facebook.com', '',
                                               'flask@django.com', 'numpy')
        url_2_response = self.user_shorten_url('https://www.google.com', '',
                                               'flask@django.com', 'numpy')

        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'short_url': url_1_response['url']['short_url']})
        self.client.post(
            url_for('api.visit'), headers=headers, data=data,
            environ_base={'HTTP_USER_AGENT': 'Chrome, windows',
                          'REMOTE_ADDR': '127.0.0.1'})
        data = json.dumps({'short_url': url_2_response['url']['short_url']})
        self.client.post(
            url_for('api.visit'), headers=headers, data=data,
            environ_base={'HTTP_USER_AGENT': 'Chrome, windows',
                          'REMOTE_ADDR': '127.0.0.1'})
        data = json.dumps({'short_url': url_2_response['url']['short_url']})
        self.client.post(
            url_for('api.visit'), headers=headers, data=data,
            environ_base={'HTTP_USER_AGENT': 'Chrome, windows',
                          'REMOTE_ADDR': '127.0.0.1'})
        response = self.client.get(url_for('api.popular'), headers=headers)
        popular_urls = json.loads(response.data)['popular_urls']
        self.assertIsInstance(popular_urls, list)
        self.assertEqual(
            popular_urls[0]['short_url'], url_2_response['url']['short_url'])
        self.assertEqual(
            popular_urls[1]['short_url'], url_1_response['url']['short_url'])

    def test_popular_with_no_url(self):
        """
        This function tests getting the response when there is no URL visited
        when getting popular URLs.
        """
        headers = {'Content-Type': 'application/json'}
        response = self.client.get(url_for('api.popular'), headers=headers)
        message = json.loads(response.data)['message']
        self.assertEqual('No URL found', message)
