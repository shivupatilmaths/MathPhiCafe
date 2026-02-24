"""Seed the database with initial data (admin user + sample subjects)."""
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import AdminUser, Subject

app = create_app()

with app.app_context():
    # Create admin user if not exists
    if not AdminUser.query.filter_by(username='admin').first():
        admin = AdminUser(
            username='admin',
            email='admin@mathphicafe.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Administrator',
            is_superadmin=True
        )
        db.session.add(admin)
        print('Admin user created: username=admin, password=admin123')
    else:
        print('Admin user already exists.')

    # Create default subjects if none exist
    if Subject.query.count() == 0:
        subjects = [
            Subject(name='Mathematics', code='MATH', description='Comprehensive mathematics coaching covering algebra, geometry, trigonometry, calculus, and more.', icon='bi-calculator', color='#6C63FF'),
            Subject(name='Physics', code='PHY', description='In-depth physics coaching covering mechanics, thermodynamics, optics, electromagnetism, and modern physics.', icon='bi-lightning', color='#FF6584'),
            Subject(name='Chemistry', code='CHEM', description='Complete chemistry coaching including organic, inorganic, and physical chemistry.', icon='bi-droplet-half', color='#00C9A7'),
            Subject(name='Biology', code='BIO', description='Thorough biology coaching covering botany, zoology, genetics, and ecology.', icon='bi-tree', color='#F59E0B'),
            Subject(name='Computer Science', code='CS', description='Programming and computer science fundamentals including Python, data structures, and algorithms.', icon='bi-cpu', color='#8B5CF6'),
        ]
        db.session.add_all(subjects)
        print('Default subjects created.')
    else:
        print('Subjects already exist.')

    db.session.commit()
    print('Database seeded successfully!')
