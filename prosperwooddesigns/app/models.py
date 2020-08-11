# models.py
# Michael Cole
#
# Database models for consumption by SQLAlchemy
# ---------------------------------------------

from flask_sqlalchemy import SQLAlchemy
from .extensions import Logger

db = SQLAlchemy()
logger = Logger()


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
        db.String(80),
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
        db.DateTime,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'Admin: @{self.username} ({self.firstname} {self.lastname})'


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
        unique=True,
        nullable=False
    )
    phonenumber = db.Column(
        db.String(80),
        unique=True,
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
        nullable=False
    )
    description = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    status = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    is_deleted = db.Column(
        db.Boolean,
        unique=False,
        nullable=False
    )
    created_date = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

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
        db.DateTime,
        unique=False,
        nullable=False
    )

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
        db.DateTime,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'Layout: {self.endpoint} - {self.content_name}'


class Contact (db.Model):
    '''
    Data model for Contact
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    emailaddress = db.Column(
        db.String(64),
        unique=True,
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
    created_date = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'Contact: {self.name} - {self.emailaddress}'
