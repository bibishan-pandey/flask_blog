import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_blog import app, mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # _ for unused variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    # resize the image
    output_size = (256, 256)
    i= Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@flask.com', recipients = [user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external = True)}
    
If you did not make this request, then simply ignore this email.
'''
    mail.send(msg)
    # note this only works for account that has not enabled two step verification and has enable access to less secure applications in the settings