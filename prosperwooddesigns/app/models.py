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
