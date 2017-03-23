import unittest
from app import create_app, db
from flask import current_app
from app.models import ShortUrl, LongUrl, User, Visitor


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com')
        self.assertTrue(user)
        user.save()
        self.assertEqual(user.user_id, 1)

    def test_add_short_url(self):
        url = ShortUrl(short_url='http://127.0.0.1/t3T1n9')
        self.assertTrue(url)
        url.save()
        self.assertTrue(url.active)
        self.assertFalse(url.deleted)

    def test_add_long_url(self):
        url = LongUrl(long_url='http://www.endurance.eu/pepperoni')
        self.assertTrue(url)
        url.save()
        self.assertEqual(url.long_url_id, 1)

    def test_add_visitor(self):
        visitor = Visitor(name='Inguinal', email='inquinal@yahoo.com')
        self.assertTrue(visitor)
        visitor.save()
        self.assertEqual(visitor.visitor_id, 1)

    def test_user_password_hash(self):
        user = User()
        user.password = 'Adela87kun'
        self.assertTrue(user.verify_password('Adela87kun'))
        self.assertFalse(user.verify_password('ela87kun'))
        self.assertRaises(AttributeError, getattr, user, 'password')

    def test_user_shorturl_relationship(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com')
        url = ShortUrl(short_url='http://127.0.0.1/t3T1n9', user=user)
        url_second = ShortUrl(short_url='www.fus.ly/hGy87T', user=user)
        db.session.add_all([user, url, url_second])
        db.session.commit()
        self.assertEqual(url.user.first_name, 'Abdul-Mumeen')
        self.assertEqual(len(user.short_urls), 2)
        self.assertEqual(user.short_urls[0].short_url, 'http://127.0.0.1/t3T1n9')
        self.assertEqual(user.short_urls[1].short_url, 'www.fus.ly/hGy87T')

    def test_shorturl_longurl_relationship(self):
        long_url = LongUrl(long_url='www.edurance.com/blogpost/1234')
        short_url = ShortUrl(short_url='www.fus.ly/hGy87T', long_url=long_url)
        short_url_2 = ShortUrl(short_url='www.fus.ly/TY65as', long_url=long_url)
        db.session.add_all([long_url, short_url, short_url_2])
        db.session.commit()
        self.assertEqual(short_url.long_url.long_url, 'www.edurance.com/blogpost/1234')
        self.assertEqual(short_url_2.long_url.long_url, 'www.edurance.com/blogpost/1234')
        self.assertEqual(len(long_url.short_urls), 2)
        self.assertEqual(long_url.short_urls[1].short_url, 'www.fus.ly/TY65as')
        self.assertEqual(long_url.short_urls[0].short_url, 'www.fus.ly/hGy87T')
        new_short_url = ShortUrl.query.filter_by(short_url_id=2).first()
        self.assertTrue(new_short_url)
        self.assertEqual(new_short_url.long_url.long_url, 'www.edurance.com/blogpost/1234')

    def test_url_vistor_relationship(self):
        visitor = Visitor(name='Peter Pan', email='peter.pan@andela.com')
        url = ShortUrl(short_url='www.fus.ly/hGy87T')
        visitor.short_urls.append(url)
        db.session.add_all([visitor, url])
        db.session.commit()
        self.assertEqual(len(list(url.visitors)), 1)
        self.assertEqual(url.visitors[0].name, 'Peter Pan')

    def test_generate_verify_token(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com', password='dGe67s')
        user.save()
        token = user.generate_auth_token(3600)
        new_user = User.verify_auth_token(token)
        self.assertEqual(user, new_user)
