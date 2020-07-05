# forms.py
# Michael Cole
#
# Forms to be used by flask_wtf to render and handle form data
# ------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    '''
    An order form for users to request a custom design.
    '''

    email = EmailField('Email', validators=[
        DataRequired()
    ])

    phone = StringField('Phone Number', validators=[
        DataRequired()
    ])

    name = StringField('Name', validators=[
        DataRequired()
    ])

    contact_method = SelectField('Preferred Contact Method', choices=[
        (None, 'No Preference'), ('email', 'Email'), ('phone', 'Phone')
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

    name = StringField('Name', validators=[
        DataRequired()
    ])

    email = StringField('Email', validators=[
        DataRequired()
    ])

    content = TextAreaField('Content', validators=[
        DataRequired()
    ])

    submit = SubmitField('Send')
