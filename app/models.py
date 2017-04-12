from datetime import datetime

from flask import current_app, url_for
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

# This is a db table that keeps the many to many relationship between
# Short URLs and their Visitors
visits = db.Table('visits',
                  db.Column('visitor_id', db.Integer,
                            db.ForeignKey('visitors.visitor_id')),
                  db.Column('short_url_id', db.Integer,
                            db.ForeignKey('short_urls.short_url_id'))
                  )


class User(UserMixin, db.Model):
    """
    This is the User model class which contains a user information an has a
    one to many relationship with the ShortUrl model.
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    short_urls = db.relationship('ShortUrl', backref='user')
    anonymous = False

    def get_id(self):
        # This returns the id of this user
        return self.user_id

    @property
    def is_anonymous(self):
        # This returns the anonymity status of the user
        return self.anonymous

    @property
    def password(self):
        # This function raise an error for accessing the user password
        raise AttributeError('password is not a readable attribute')

    def generate_auth_token(self, expiration):
        # This generates a user token base on the user id
        s = Serializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        # This function verifies the token supplied by the user
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['user_id'])

    @password.setter
    def password(self, password):
        # This function sets the user password hash from the password supplied
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # This function verifies the user password against its hash
        return check_password_hash(self.password_hash, password)

    def save(self):
        # This function save the user details to the database.
        db.session.add(self)
        db.session.commit()

    def get_details(self):
        # This function returns the details of the current user
        user_details = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'short_urls': [
                url_for('api.shorturls', _external=True) +
                str(short_url.short_url_id)
                for short_url in self.short_urls
            ]}
        return user_details

    def __repr__(self):
        # This returns a machine representation of a user
        return '<User %r>' % (self.first_name + " " + self.last_name)


class ShortUrl(db.Model):
    """
    This is the short url which has a many to many relationship with the
    Visitor model and a many to one to the User model.
    """
    __tablename__ = 'short_urls'
    short_url_id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(64), unique=True)
    active = db.Column(db.Integer, index=True, default=1)
    deleted = db.Column(db.Integer, default=0)
    date_time = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    long_url_id = db.Column(db.Integer, db.ForeignKey('long_urls.long_url_id'))

    def save(self):
        # This saves the short URL into the database
        db.session.add(self)
        db.session.commit()

    def get_details(self):
        # This returns the short url details as a json object
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
        # This returns a machine representation of the short url
        return '<Url %r>' % self.short_url


class LongUrl(db.Model):
    """
    This is the Long URL model which has a one to many relationship with the
    Short URl model.
    """
    __tablename__ = 'long_urls'
    long_url_id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text, index=True)
    short_urls = db.relationship(
        'ShortUrl', backref='long_url', lazy='dynamic')

    def save(self):
        # This saves the long URL details in the database
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # This returns a machine representation of a long URL
        return '<Url %r>' % self.long_url


class Visitor(db.Model):
    """
    This is the Visitors model which holds information of a visitor to a URL.
    It has many to many relationship with the ShortUrl model
    """
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
        # This saves the visitor details in the database
        db.session.add(self)
        db.session.commit()

    def get_details(self):
        # This function returns a visitor's details as a json object
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
        # This returns a machine representation of a visitor
        return '<Visitor %r>' % self.ip_address
