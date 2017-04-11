import json
from datetime import datetime

from flask import current_app, jsonify, url_for
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

visits = db.Table('visits',
                  db.Column('visitor_id', db.Integer,
                            db.ForeignKey('visitors.visitor_id')),
                  db.Column('short_url_id', db.Integer,
                            db.ForeignKey('short_urls.short_url_id'))
                  )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    short_urls = db.relationship('ShortUrl', backref='user')
    anonymous = False

    def get_id(self):
        return self.user_id

    @property
    def is_anonymous(self):
        return self.anonymous

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def generate_auth_token(self, expiration):
        s = Serializer(
            current_app.config['SECRET_KEY'],  expires_in=expiration)
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
        return '<User %r>' % (self.first_name + " " + self.last_name)


class ShortUrl(db.Model):
    __tablename__ = 'short_urls'
    short_url_id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(64), unique=True)
    active = db.Column(db.Integer, index=True, default=1)
    deleted = db.Column(db.Integer, default=0)
    date_time = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    long_url_id = db.Column(db.Integer, db.ForeignKey('long_urls.long_url_id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_details(self):
        visit = db.session.query(ShortUrl, db.func.count(
            visits.c.short_url_id)).outerjoin(visits).group_by(
            ShortUrl.short_url_id).filter_by(
            short_url_id=self.short_url_id).first()
        no_of_visits = visit[1] if visit else 0
        url_details = {
            'short_url': self.short_url,
            'short_url_url': url_for(
                'api.shorturl', id=self.short_url_id, _external=True),
            'long_url': self.long_url.long_url,
            'number_of_visits': no_of_visits,
            'visitors': [
                url_for('api.visitor', vid=visitor.visitor_id,
                        id=self.short_url_id,
                        _external=True) for visitor in self.visitors]
        }
        return url_details

    def __repr__(self):
        return '<Url %r>' % self.short_url


class LongUrl(db.Model):
    __tablename__ = 'long_urls'
    long_url_id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text, index=True)
    short_urls = db.relationship(
        'ShortUrl', backref='long_url', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Url %r>' % self.long_url


class Visitor(db.Model):
    __tablename__ = 'visitors'
    visitor_id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64))
    browser = db.Column(db.String(64), index=True)
    platform = db.Column(db.String(64), index=True)
    short_urls = db.relationship('ShortUrl', secondary=visits,
                                 backref=db.backref(
                                     'visitors', lazy='dynamic'),
                                 lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_details(self):
        details = {
            'ip_address': self.ip_address,
            'browser': self.browser,
            'platform': self.platform,
            'short_urls': [
                url_for('api.shorturls', _external=True) +
                str(short_url.short_url_id)
                for short_url in self.short_urls
            ]
        }
        return details

    def __repr__(self):
        return '<Visitor %r>' % self.ip_address
