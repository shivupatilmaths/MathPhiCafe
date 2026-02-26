import os

basedir = os.path.abspath(os.path.dirname(__file__))

# On Fly.io a persistent volume is mounted at /data; fall back to local paths
_data_dir = os.environ.get('PERSISTENT_DATA_DIR') or os.path.join(basedir, 'instance')
_uploads_dir = os.environ.get('PERSISTENT_UPLOADS_DIR') or os.path.join(basedir, 'app', 'static', 'uploads')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mathphi-cafe-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(_data_dir, 'mathphi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    UPLOAD_FOLDER = _uploads_dir
    GALLERY_FOLDER = os.path.join(_uploads_dir, 'gallery')
    NOTES_FOLDER = os.path.join(_uploads_dir, 'notes')
    AVATARS_FOLDER = os.path.join(_uploads_dir, 'avatars')
    THUMBNAILS_FOLDER = os.path.join(_uploads_dir, 'thumbnails')

    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_NOTE_EXTENSIONS = {'pdf'}
