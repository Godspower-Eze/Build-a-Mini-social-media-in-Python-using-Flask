from flask_mail import Message
from socialmedia import mail
from flask import url_for, current_app
import secrets, os
from PIL import Image

thumnail_size = (300, 300)


def send_reset_token(user):
    token = user.get_reset_token()
    msg = Message('Password reset email',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f"{url_for('reset_token', token=token, _external=True)}" \
               f"if you did not not request for this please ignore"
    mail.send(msg)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_image', picture_fn)
    image = Image.open(form_picture)
    image.thumbnail(thumnail_size)
    image.save(picture_path)
    return picture_fn
