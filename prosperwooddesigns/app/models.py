# models.py
# Michael Cole
#
# Database models for consumption by SQLAlchemy
# ---------------------------------------------

from datetime import datetime

from app.extensions.Logger import Logger
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Instantiate variables
logger = Logger()
db = SQLAlchemy()
loginManager = LoginManager()


# User Loader used by flask_login
@loginManager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id=admin_id).first()


class Admin(db.Model):
    '''
    Data model for Admin
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(),
        unique=False,
        nullable=False
    )
    firstname = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    lastname = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, username, password, firstname,
        lastname, created_date=datetime.now()
    ):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.created_date = created_date  # current time by default

    def __repr__(self):
        return f'Admin: @{self.username} ({self.firstname} {self.lastname})'

    # below 4 methods are for flask_login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Request(db.Model):
    '''
    Data model for Request
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    emailaddress = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    phonenumber = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    name = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    contactmethod = db.Column(
        db.String(80),
        unique=False,
        nullable=True
    )
    description = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    how_hear = db.Column(
        db.String(80),
        unique=False,
        nullable=True
    )
    status = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    is_archived = db.Column(
        db.Boolean,
        unique=False,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, emailaddress, phonenumber, name, contactmethod,
        description, how_hear, status, is_archived=False,
        created_date=datetime.now()
    ):
        self.emailaddress = emailaddress
        self.phonenumber = phonenumber
        self.name = name
        self.contactmethod = contactmethod
        self.description = description
        self.how_hear = how_hear
        self.status = status
        self.is_archived = is_archived  # False by default
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Request: {self.name} - {self.emailaddress} ({self.status})'


class Image(db.Model):
    '''
    Data model for Image
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    description = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    filename = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, name, description, filename, created_date=datetime.now()
    ):
        self.name = name
        self.description = description
        self.filename = filename
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Image: {self.name}'


class Layout(db.Model):
    '''
    Data model for Layout
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    endpoint = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    content_name = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    content = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )
    is_image = db.Column(
        db.Boolean,
        unique=False,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, endpoint, content_name, content,
        is_image, created_date=datetime.now()
    ):
        self.endpoint = endpoint
        self.content_name = content_name
        self.content = content
        self.is_image = is_image
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Layout: {self.endpoint} - {self.content_name}'


class Question(db.Model):
    '''
    Data model for Question
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    emailaddress = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    name = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    content = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    how_hear = db.Column(
        db.String(80),
        unique=False,
        nullable=True
    )
    status = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    is_archived = db.Column(
        db.Boolean,
        unique=False,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, emailaddress, name, content, how_hear, status,
        is_archived=False, created_date=datetime.now()
    ):
        self.emailaddress = emailaddress
        self.name = name
        self.content = content
        self.how_hear = how_hear
        self.status = status
        self.is_archived = is_archived  # false by default
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Question: {self.name} - {self.emailaddress} ({self.status})'


class Contact(db.Model):
    '''
    Data model for Contact
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    phonenumber = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    emailaddress = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )

    def __init__(self, name, phonenumber=False, emailaddress=False):
        self.name = name
        self.phonenumber = phonenumber
        self.emailaddress = emailaddress

    def __repr__(self):
        return f'Contact: {self.name}'
