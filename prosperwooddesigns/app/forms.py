# forms.py
# Michael Cole
#
# Forms to be used by flask_wtf to render and handle form data
# ------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional,
                                Regexp, ValidationError)

from app.extensions.DbConnector import DbConnector

dbConn = DbConnector()


def email_or_phone(form, field):
    if len(form.phone.data) == 0 and len(form.email.data) == 0:
        raise ValidationError(
            'Must provide either a phone number or an email address'
        )


def username_not_found(form, field):
    user = dbConn.getAdmin(username=field.data)
    if not user:
        raise ValidationError("Username doesn't exist")


def username_exists(form, field):
    user = dbConn.getAdmin(username=field.data)
    if user:
        raise ValidationError("Username already taken")


def incorrect_password(form, field):
    username = form.username.data
    user = dbConn.getAdmin(username=username)
    if user:
        import flask_bcrypt
        if not flask_bcrypt.check_password_hash(user.password, field.data):
            raise ValidationError("Incorrect password")


def secret_code_check(form, field):
    from os import environ
    if not field.data == environ['ADMIN_FORM_SECRET_CODE']:
        raise ValidationError('Incorrect secret code')


class RequestForm(FlaskForm):
    '''
    A request form for users to request a custom design.
    '''

    email = StringField('Your Email', validators=[
        email_or_phone,
        Optional(),
        Email()
    ])

    phone = StringField('Your Phone Number', validators=[
        email_or_phone
    ])

    name = StringField('Your Name', validators=[
        DataRequired(),
    ])

    contact_method = SelectField('Your Preferred Contact Method', choices=[
        ('phone', 'Phone'), ('email', 'Email'), (None, 'No Preference')
    ], validators=[
        DataRequired()
    ])

    how_hear = StringField('How Did You Hear About Us?')

    description = TextAreaField("Tell me what you're looking for!",
                                validators=[
                                    DataRequired()
                                    ]
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
        DataRequired(),
        Email()
    ])

    how_hear = StringField('How Did You Hear About Us?')

    content = TextAreaField('Question', validators=[
        DataRequired()
    ])

    submit = SubmitField('Send')


class AdminLogInForm(FlaskForm):
    '''
    Admin Log-In Form for an admin to log-in to the site
    '''

    username = StringField('Username', validators=[
        DataRequired(),
        username_not_found
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        incorrect_password
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
        DataRequired(),
        Length(min=5, max=20,
               message="Username must be between 5 and 20 characters"
               ),
        username_exists
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})',
            message=(
                "Password must contain the following:<br>"
                "<ul>"
                "<li>At least 8 characters</li>"
                "<li>At least 1 lowercase alphabetical character</li>"
                "<li>At least 1 uppercase alphabetical character</li>"
                "<li>At least 1 numeric character</li>"
                "<li>At least 1 special character [!@#$%^&*]</li>"
                "</ul>")
        ),
        Length(min=8, message='Password must contain at least 8 characters'),
    ])

    password_retype = PasswordField('Retype Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords do not match')
    ])

    secret_code = PasswordField('Secret Code', validators=[
        DataRequired(),
        secret_code_check
    ])

    submit = SubmitField('Create Account')
