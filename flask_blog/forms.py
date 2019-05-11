from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=20)])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=8, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # custom validation
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken!')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken!')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=20)])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')

# after this step setup the secret key in the app
# good way to generate secret key is to open python interpretor and import secrets and use secrets.token_hex(16)
# and import these forms from main app and create routes for it

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=20)])
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['png','jpg'])])

    submit = SubmitField('Update')

    # custom validation
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken!')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken!')

class PostForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')

    submit = SubmitField('Post')

    # custom validation
    def validate_title(self, title):
        if title.data == '':
            raise ValidationError('Title is required!')
    
    def validate_content(self, content):
        if content.data == '':
            raise ValidationError('Content is required!')