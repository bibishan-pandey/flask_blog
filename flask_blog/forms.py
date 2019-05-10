from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=20)])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=8, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=20)])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')

# after this step setup the secret key in the app
# good way to generate secret key is to open python interpretor and import secrets and use secrets.token_hex(16)
# and import these forms from main app and create routes for it