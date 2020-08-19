# forms.py
# Michael Cole
#
# Forms to be used by flask_wtf to render and handle form data
# ------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RequestForm(FlaskForm):
    '''
    A request form for users to request a custom design.
    '''

    email = EmailField('Your Email', validators=[
        DataRequired()
    ])

    phone = StringField('Your Phone Number', validators=[
        DataRequired()
    ])

    name = StringField('Your Name', validators=[
        DataRequired()
    ])

    contact_method = SelectField('Your Preferred Contact Method', choices=[
        ('phone', 'Phone'), ('email', 'Email'), (None, 'No Preference')
    ], validators=[
        DataRequired()
    ])

    description = TextAreaField("Tell me what you're looking for!",
                                validators=[DataRequired()]
                                )

    submit = SubmitField('Request')


class ContactForm(FlaskForm):
    '''
    Contact Form for users to communicate with the owner without
    requesting a design
    '''

    name = StringField('Your Name', validators=[
        DataRequired()
    ])

    email = StringField('Your Email', validators=[
        DataRequired()
    ])

    content = TextAreaField('Question', validators=[
        DataRequired()
    ])

    submit = SubmitField('Send')


class AdminLogInForm(FlaskForm):
    '''
    Admin Log-In Form for an admin to log-in to the site
    '''

    username = StringField('Username', validators=[
        DataRequired()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    submit = SubmitField('Log-In')


class AdminCreateForm(FlaskForm):
    '''
    Admin Create Form for an admin to create an admin account in the site
    '''

    firstname = StringField('First Name', validators=[
        DataRequired()
    ])

    lastname = StringField('Last Name', validators=[
        DataRequired()
    ])

    username = StringField('Username', validators=[
        DataRequired()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    password_retype = PasswordField('Retype Password', validators=[
        DataRequired()
    ])

    secret_code = PasswordField('Secret Code', validators=[
        DataRequired()
    ])

    submit = SubmitField('Create Account')
