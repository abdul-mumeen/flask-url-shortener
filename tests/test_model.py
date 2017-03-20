import unittest
from app import create_app, db
from flask import current_app
from app.models import Url, User, Visitor


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
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.user_id, 1)

    def test_add_url(self):
        url = Url(short_url='http://127.0.0.1/t3T1n9',
                  long_url='www.edurance.com/blogpost/1234')

        self.assertTrue(url)
        db.session.add(url)
        db.session.commit()
        self.assertTrue(url.active)
        self.assertFalse(url.deleted)

    def test_add_visitor(self):
        visitor = Visitor(name='Inguinal', email='inquinal@yahoo.com')
        self.assertTrue(visitor)
        db.session.add(visitor)
        db.session.commit()
        self.assertEqual(visitor.visitor_id, 1)

    def test_user_password_hash(self):
        user = User()
        user.password = 'Adela87kun'
        self.assertTrue(user.verify_password('Adela87kun'))
        self.assertFalse(user.verify_password('ela87kun'))
        self.assertRaises(AttributeError, getattr, user, 'password')

    def test_user_url_relationship(self):
        user = User(first_name='Abdul-Mumeen', last_name='Olasode',
                    email='abdulmumeen.olasode@andela.com')
        url = Url(short_url='http://127.0.0.1/t3T1n9',
                  long_url='www.edurance.com/blogpost/1234', user=user)
        url_second = Url(short_url='www.fus.ly/hGy87T',
                         long_url='www.barrow.com/post/1234', user=user)
        db.session.add_all([user, url])
        db.session.commit()
        self.assertEqual(url.user.first_name, 'Abdul-Mumeen')
        self.assertEqual(len(user.urls), 2)
        self.assertEqual(user.urls[0].short_url, 'http://127.0.0.1/t3T1n9')
        self.assertEqual(user.urls[1].short_url, 'www.fus.ly/hGy87T')

    def test_url_vistor_relationship(self):
        visitor = Visitor(name='Peter Pan', email='peter.pan@andela.com')
        url = Url(short_url='www.fus.ly/hGy87T',
                  long_url='www.barrow.com/post/1234')
        visitor.urls.append(url)
        db.session.add_all([visitor, url])
        db.session.commit()
        self.assertEqual(len(list(url.visitors)), 1)
        self.assertEqual(url.visitors[0].name, 'Peter Pan')
