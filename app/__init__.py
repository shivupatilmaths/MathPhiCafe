import os
from flask import Flask, render_template
from .extensions import db, login_manager, migrate, csrf
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from .blueprints.public import public_bp
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp
    from .blueprints.student import student_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')

    # Make site settings available in all templates
    @app.context_processor
    def inject_settings():
        from .models import SiteSetting
        settings = {}
        try:
            for s in SiteSetting.query.all():
                settings[s.key] = s.value
        except Exception:
            pass
        return dict(site_settings=settings)

    # Create instance directory, tables, and upload directories
    with app.app_context():
        # Ensure the instance directory exists for SQLite database
        instance_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance')
        os.makedirs(instance_path, exist_ok=True)

        db.create_all()
        for folder_key in ['GALLERY_FOLDER', 'NOTES_FOLDER', 'AVATARS_FOLDER', 'THUMBNAILS_FOLDER']:
            path = app.config.get(folder_key, '')
            if path:
                os.makedirs(path, exist_ok=True)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app
