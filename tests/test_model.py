import unittest

from app import create_app, db
from app.models import LongUrl, ShortUrl, User, Visitor


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        """
        This function runs before each test initializing the application and
        creating a client that will consume it.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        This function runs after each test removing the session and destroying
        the table that might have been created during testing.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        """
        This function tests adding a user to the User model.
        """
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com')
        self.assertTrue(user)
        user.save()
        self.assertEqual(user.user_id, 1)
        self.assertEqual(repr(user), '<User: Abdul-Mumeen Olasode>')

    def test_add_short_url(self):
        """
        This function tests adding a shorl URL to the ShortUrl model.
        """
        url = ShortUrl(short_url='http://127.0.0.1/t3T1n9')
        self.assertTrue(url)
        url.save()
        self.assertTrue(url.active)
        self.assertFalse(url.deleted)
        self.assertEqual(repr(url), '<ShortUrl: http://127.0.0.1/t3T1n9>')

    def test_add_long_url(self):
        """
        This function tests adding a long URL to the LongUrl model.
        """
        url = LongUrl(long_url='http://www.endurance.eu/pepperoni')
        self.assertTrue(url)
        url.save()
        self.assertEqual(url.long_url_id, 1)
        self.assertEqual(repr(url),
                         '<LongUrl: http://www.endurance.eu/pepperoni>')

    def test_add_visitor(self):
        """
        This function tests adding a visitor to the Visitor model.
        """
        visitor = Visitor(ip_address='198.168.1.1', browser='mozilla',
                          platform='windows')
        self.assertTrue(visitor)
        visitor.save()
        self.assertEqual(visitor.visitor_id, 1)
        self.assertEqual(repr(visitor), '<Visitor: 198.168.1.1>')

    def test_user_password_hash(self):
        """
        This function is used to test the successful hashing of the password
        supplied by the user.
        """
        user = User()
        user.password = 'Adela87kun'
        self.assertTrue(user.verify_password('Adela87kun'))
        self.assertFalse(user.verify_password('ela87kun'))
        self.assertRaises(AttributeError, getattr, user, 'password')

    def test_user_shorturl_relationship(self):
        """
        This function is used to test the model relationship between the user
        and their respective shortened URLs.
        """
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com')
        url = ShortUrl(short_url='http://127.0.0.1/t3T1n9', user=user)
        url_second = ShortUrl(short_url='www.fus.ly/hGy87T', user=user)
        db.session.add_all([user, url, url_second])
        db.session.commit()
        self.assertEqual(url.user.first_name, 'Abdul-Mumeen')
        self.assertEqual(len(user.short_urls), 2)
        self.assertEqual(
            user.short_urls[0].short_url, 'http://127.0.0.1/t3T1n9')
        self.assertEqual(user.short_urls[1].short_url, 'www.fus.ly/hGy87T')

    def test_shorturl_longurl_relationship(self):
        """
        This function is used to test the various model relationship between
        a short URL and its targetted long URL.
        """
        long_url = LongUrl(long_url='www.edurance.com/blogpost/1234')
        short_url = ShortUrl(short_url='www.fus.ly/hGy87T', long_url=long_url)
        short_url_2 = ShortUrl(
            short_url='www.fus.ly/TY65as', long_url=long_url)
        db.session.add_all([long_url, short_url, short_url_2])
        db.session.commit()
        self.assertEqual(short_url.long_url.long_url,
                         'www.edurance.com/blogpost/1234')
        self.assertEqual(short_url_2.long_url.long_url,
                         'www.edurance.com/blogpost/1234')
        self.assertEqual(len(long_url.short_urls.all()), 2)
        self.assertEqual(long_url.short_urls[1].short_url, 'www.fus.ly/TY65as')
        self.assertEqual(long_url.short_urls[0].short_url, 'www.fus.ly/hGy87T')
        new_short_url = ShortUrl.query.filter_by(short_url_id=2).first()
        self.assertTrue(new_short_url)
        self.assertEqual(new_short_url.long_url.long_url,
                         'www.edurance.com/blogpost/1234')

    def test_url_vistor_relationship(self):
        """
        This function is used to test the model relationship between a short
        URL and visitors to the URL.
        """
        visitor = Visitor(ip_address='198.168.1.1', browser='mozilla',
                          platform='windows')
        url = ShortUrl(short_url='www.fus.ly/hGy87T')
        visitor.short_urls.append(url)
        db.session.add_all([visitor, url])
        db.session.commit()
        self.assertEqual(len(list(url.visitors)), 1)
        self.assertEqual(url.visitors[0].ip_address, '198.168.1.1')

    def test_generate_verify_token(self):
        """
        This function is used to test the verification of the token generated
        for a user.
        """
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com', password='dGe67s')
        user.save()
        token = user.generate_auth_token(3600)
        new_user = User.verify_auth_token(token)
        self.assertEqual(user, new_user)
