from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from datetime import datetime, timedelta


class User(db.Model):
    """
    Create an Employee table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_login_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean(), default=False)

    calendar = db.relationship("Calendar")

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        if self.last_login_date:
            last_login = self.last_login_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_login = None
        return {'id': self.id,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'last_login': last_login,
                'status': 'logged-in' if self.active else 'logged-out'}

    def __repr__(self):
        return 'Users(id={}, {}, {}, {}, status={})'\
                .format(self.id,
                        self.email,
                        self.first_name,
                        self.last_name,
                        self.active)


class Calendar(db.Model):
    """
    Create a Calendar table
    """

    __tablename__ = 'calendars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    event = db.relationship("Event", cascade="all,delete", backref="parent")

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'owner': self.user_id}

    def __repr__(self):
        return 'Calendar(id={}, {}, {}, owner={})'\
                .format(self.id,
                        self.name,
                        self.description,
                        self.user_id)


class Event(db.Model):
    """
    Create a Event table
    """

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.now(), index=True)
    end_date = db.Column(db.DateTime,
                         default=datetime.now() + timedelta(hours=1),
                         index=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendars.id'))

    def serialize(self):
        return {'id': self.id,
                'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_date': self.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'title': self.title,
                'description': self.description,
                'calendar': self.calendar_id}

    def __repr__(self):
        return 'Event(id={}, {}, {}, {}, {}, calendar={})' \
                .format(self.id,
                        self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                        self.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                        self.title,
                        self.description,
                        self.calendar_id)
