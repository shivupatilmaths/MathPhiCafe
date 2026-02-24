import os
import random
import string
from functools import wraps
from datetime import datetime

from flask import abort, current_app
from flask_login import current_user
from PIL import Image


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def generate_student_id():
    from .models import Student
    year = datetime.now().year
    last = Student.query.filter(
        Student.student_id.like(f'MPC-{year}-%')
    ).order_by(Student.id.desc()).first()

    if last:
        num = int(last.student_id.split('-')[-1]) + 1
    else:
        num = 1
    return f'MPC-{year}-{num:03d}'


def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def calculate_grade(percentage):
    if percentage >= 91:
        return 'A1'
    elif percentage >= 81:
        return 'A2'
    elif percentage >= 71:
        return 'B1'
    elif percentage >= 61:
        return 'B2'
    elif percentage >= 51:
        return 'C1'
    elif percentage >= 41:
        return 'C2'
    elif percentage >= 33:
        return 'D'
    else:
        return 'E'


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_image(file, folder, max_size=(800, 800)):
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = os.path.splitext(filename)
    unique_name = f'{name}_{timestamp}{ext}'
    filepath = os.path.join(folder, unique_name)

    img = Image.open(file)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(filepath, quality=85, optimize=True)

    return unique_name


def create_thumbnail(source_path, thumb_folder, size=(300, 300)):
    filename = os.path.basename(source_path)
    thumb_path = os.path.join(thumb_folder, f'thumb_{filename}')

    img = Image.open(source_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail(size, Image.LANCZOS)
    img.save(thumb_path, quality=80, optimize=True)

    return f'thumb_{filename}'


def save_file(file, folder):
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = os.path.splitext(filename)
    unique_name = f'{name}_{timestamp}{ext}'
    filepath = os.path.join(folder, unique_name)
    file.save(filepath)
    return unique_name, os.path.getsize(filepath)
