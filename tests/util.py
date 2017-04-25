import json
from base64 import b64encode

from flask import url_for

from app import create_app, db
from app.models import User


class UserDetailHelper(object):
    def set_up(self):
        """
        This function initializes the application, creating tables in the db
        and creating a client that will consume it.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tear_down(self):
        """
        This function delete the session and destroys tables that might have
        been created during testing.
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
