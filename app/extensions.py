from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from .models import AdminUser, Student
    kind, uid = user_id.split(':', 1)
    if kind == 'admin':
        return db.session.get(AdminUser, int(uid))
    elif kind == 'student':
        return db.session.get(Student, int(uid))
    return None
