from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(20))
    urls = db.relationship('Url', backref='user')

    def __repr__(self):
        return '<User %r>' % self.first_name + " " + self.last_name


class Url(db.Model):
    __tablename__ = 'urls'
    url_id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(64), unique=True)
    long_url = db.Column(db.Text, index=True)
    active = db.Column(db.Integer index=True)
    deleted = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Url %r>' % self.short_url


class Visitor(db.Model):
    __tablename__ = 'visitor'
    vistor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Visitor %r>' % self.name
