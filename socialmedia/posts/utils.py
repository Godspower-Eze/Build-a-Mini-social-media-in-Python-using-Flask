import os, secrets
from PIL import Image
from flask import current_app

thumnail_size = (300, 300)


def postsave_picture(post_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(post_picture.filename)
    print(post_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_image', picture_fn)
    image = Image.open(post_picture)
    image.thumbnail(thumnail_size)
    image.save(picture_path)
    return picture_fn
