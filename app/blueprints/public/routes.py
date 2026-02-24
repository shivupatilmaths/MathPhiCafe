from flask import render_template, flash, redirect, url_for, request
from . import public_bp
from ...models import Subject, Faculty, GalleryImage, Announcement, Testimonial, ContactMessage
from ...forms import ContactForm
from ...extensions import db


@public_bp.route('/')
def home():
    subjects = Subject.query.filter_by(is_active=True).all()
    testimonials = Testimonial.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    announcements = Announcement.query.filter_by(is_active=True).order_by(
        Announcement.created_at.desc()
    ).limit(5).all()
    from ...models import Student, Batch
    stats = {
        'students': Student.query.filter_by(is_active=True).count(),
        'faculty': Faculty.query.filter_by(is_active=True).count(),
        'batches': Batch.query.filter_by(is_active=True).count(),
    }
    return render_template('public/home.html', subjects=subjects,
                           testimonials=testimonials, announcements=announcements,
                           stats=stats)


@public_bp.route('/about')
def about():
    faculty = Faculty.query.filter_by(is_active=True).order_by(Faculty.sort_order).all()
    return render_template('public/about.html', faculty=faculty)


@public_bp.route('/subjects')
def subjects():
    subjects = Subject.query.filter_by(is_active=True).all()
    return render_template('public/subjects.html', subjects=subjects)


@public_bp.route('/subjects/<code>')
def subject_detail(code):
    subject = Subject.query.filter_by(code=code, is_active=True).first_or_404()
    from ...models import Batch
    batches = Batch.query.filter_by(subject_id=subject.id, is_active=True).all()
    faculty_ids = [b.faculty_id for b in batches if b.faculty_id]
    faculty = Faculty.query.filter(Faculty.id.in_(faculty_ids)).all() if faculty_ids else []
    return render_template('public/subject_detail.html', subject=subject,
                           batches=batches, faculty=faculty)


@public_bp.route('/faculty')
def faculty():
    faculty = Faculty.query.filter_by(is_active=True).order_by(Faculty.sort_order).all()
    return render_template('public/faculty.html', faculty=faculty)


@public_bp.route('/gallery')
def gallery():
    images = GalleryImage.query.filter_by(is_active=True).order_by(
        GalleryImage.sort_order, GalleryImage.uploaded_at.desc()
    ).all()
    categories = db.session.query(GalleryImage.category).filter_by(
        is_active=True
    ).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('public/gallery.html', images=images, categories=categories)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html', form=form)


@public_bp.route('/testimonials')
def testimonials():
    testimonials = Testimonial.query.filter_by(is_active=True).order_by(
        Testimonial.created_at.desc()
    ).all()
    return render_template('public/testimonials.html', testimonials=testimonials)
