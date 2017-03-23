from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import db
import json


visits = db.Table('visits',
                  db.Column('visitor_id', db.Integer, db.ForeignKey('visitors.visitor_id')),
                  db.Column('url_id', db.Integer, db.ForeignKey('urls.url_id'))
                  )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    urls = db.relationship('Url', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],  expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['user_id'])

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.first_name + " " + self.last_name


class Url(db.Model):
    __tablename__ = 'urls'
    url_id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(64), unique=True)
    long_url = db.Column(db.Text, index=True)
    active = db.Column(db.Integer, index=True, default=1)
    deleted = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Url %r>' % self.short_url


class Visitor(db.Model):
    __tablename__ = 'visitors'
    visitor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    urls = db.relationship('Url', secondary=visits,
                           backref=db.backref('visitors', lazy='dynamic'),
                           lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Visitor %r>' % self.name
