import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mathphi-cafe-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'mathphi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    GALLERY_FOLDER = os.path.join(UPLOAD_FOLDER, 'gallery')
    NOTES_FOLDER = os.path.join(UPLOAD_FOLDER, 'notes')
    AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, 'avatars')
    THUMBNAILS_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbnails')

    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_NOTE_EXTENSIONS = {'pdf'}
