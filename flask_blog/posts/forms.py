from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

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