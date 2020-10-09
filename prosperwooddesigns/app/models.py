# models.py
# Michael Cole
#
# Database models for consumption by SQLAlchemy
# ---------------------------------------------

from datetime import datetime

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.extensions.Logger import Logger
from app.extensions.Helper import Helper

# Instantiate variables
logger = Logger()
db = SQLAlchemy()
loginManager = LoginManager()
helper = Helper()


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


class Image(db.Model):
    '''
    Data model for Image
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    location = db.Column(
        db.String(512),
        unique=True,
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        unique=False
    )
    is_featured_img = db.Column(
        db.Boolean,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(
        self, location, product_id, is_featured_img=False,
        created_date=datetime.now()
    ):
        self.location = location
        self.product_id = product_id
        self.is_featured_img = is_featured_img
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Image: {self.location}'


class Layout(db.Model):
    '''
    Data model for Layout
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    location = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    name = db.Column(
        db.String(64),
        unique=False,
        nullable=False
    )
    content = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )
    content_html = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    def __init__(
        self, location, name, content
    ):
        self.location = location
        self.name = name
        self.content = content
        self.content_html = helper.to_html(content)

    def __repr__(self):
        return f'Layout: {self.location} - {self.name}'


class Product(db.Model):
    '''
    Data model for Product
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
    description = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    description_html = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )
    is_featured_product = db.Column(
        db.Boolean,
        nullable=False
    )
    created_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )

    def __init__(self, name, description, is_featured_product=False,
                 created_date=datetime.now()):
        self.name = name
        self.description = description
        self.description_html = helper.to_html(description)
        self.is_featured_product = is_featured_product
        self.created_date = created_date

    def __repr__(self):
        return f'Product: {self.name}'


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
    content_html = db.Column(
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
        self.content_html = helper.to_html(content)
        self.how_hear = how_hear
        self.status = status
        self.is_archived = is_archived  # false by default
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Question: {self.name} - {self.emailaddress} ({self.status})'


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
    description_html = db.Column(
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
        self.description_html = helper.to_html(description)
        self.how_hear = how_hear
        self.status = status
        self.is_archived = is_archived  # False by default
        self.created_date = created_date  # current date by default

    def __repr__(self):
        return f'Request: {self.name} - {self.emailaddress} ({self.status})'


class Visitor(db.Model):
    '''
    Data model for Visitor
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    ipaddress = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )
    first_visit_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )
    most_recent_visit_date = db.Column(
        db.Date,
        unique=False,
        nullable=False
    )
    num_visits = db.Column(
        db.Integer,
        unique=False,
        nullable=False
    )
    is_admin = db.Column(
        db.Boolean,
        unique=False,
        nullable=False
    )

    def __init__(
        self, ipaddress,
        first_visit_date=datetime.now(),
        most_recent_visit_date=datetime.now(),
        num_visits=1, is_admin=False
    ):
        self.ipaddress = ipaddress
        # first_visit and most_recent_visit are current by default
        self.first_visit_date = first_visit_date
        self.most_recent_visit_date = most_recent_visit_date
        self.num_visits = num_visits
        self.is_admin = is_admin

    def __repr__(self):
        return f'Visitor: {self.ipaddress} ({self.num_visits} visits)'
