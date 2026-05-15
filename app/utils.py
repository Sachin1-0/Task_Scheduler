import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_attachment(form_file):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_file.filename)
    _, f_ext = os.path.splitext(filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/uploads', file_fn)
    form_file.save(file_path)
    return file_fn
