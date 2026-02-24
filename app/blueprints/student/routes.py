import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import student_bp
from ...extensions import db
from ...models import (
    Student, Result, Note, Announcement, BatchEnrollment, Subject
)
from ...forms import ProfileForm, ChangePasswordForm
from ...utils import student_required, save_image


@student_bp.route('/')
@login_required
@student_required
def dashboard():
    announcements = Announcement.query.filter(
        Announcement.is_active == True,
        db.or_(
            Announcement.target_grade == None,
            Announcement.target_grade == current_user.grade
        )
    ).order_by(Announcement.created_at.desc()).limit(5).all()

    enrollments = BatchEnrollment.query.filter_by(
        student_id=current_user.id
    ).all()
    batches = [e.batch for e in enrollments if e.batch.is_active]

    recent_results = Result.query.filter_by(
        student_id=current_user.id
    ).order_by(Result.exam_date.desc()).limit(5).all()

    return render_template('student/dashboard.html',
                           announcements=announcements,
                           batches=batches,
                           recent_results=recent_results)


@student_bp.route('/results')
@login_required
@student_required
def results():
    subject_filter = request.args.get('subject', 0, type=int)
    query = Result.query.filter_by(student_id=current_user.id)
    if subject_filter:
        query = query.filter_by(subject_id=subject_filter)
    results = query.order_by(Result.exam_date.desc()).all()
    subjects = Subject.query.filter_by(is_active=True).all()
    return render_template('student/results.html', results=results,
                           subjects=subjects, subject_filter=subject_filter)


@student_bp.route('/notes')
@login_required
@student_required
def notes():
    subject_filter = request.args.get('subject', 0, type=int)
    query = Note.query.filter_by(is_active=True, grade=current_user.grade)
    if subject_filter:
        query = query.filter_by(subject_id=subject_filter)
    notes = query.order_by(Note.subject_id, Note.chapter).all()
    subjects = Subject.query.filter_by(is_active=True).all()
    return render_template('student/notes.html', notes=notes,
                           subjects=subjects, subject_filter=subject_filter)


@student_bp.route('/notes/<int:id>/download')
@login_required
@student_required
def download_note(id):
    note = Note.query.get_or_404(id)
    filepath = os.path.join(current_app.config['NOTES_FOLDER'], note.filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True,
                         download_name=f'{note.title}.pdf')
    flash('File not found.', 'danger')
    return redirect(url_for('student.notes'))


@student_bp.route('/schedule')
@login_required
@student_required
def schedule():
    enrollments = BatchEnrollment.query.filter_by(
        student_id=current_user.id
    ).all()
    batches = [e.batch for e in enrollments if e.batch.is_active]
    return render_template('student/schedule.html', batches=batches)


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    form = ProfileForm(obj=current_user)
    pw_form = ChangePasswordForm()

    if 'update_profile' in request.form and form.validate_on_submit():
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        if form.avatar.data:
            current_user.avatar = save_image(
                form.avatar.data, current_app.config['AVATARS_FOLDER'],
                max_size=(300, 300)
            )
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('student.profile'))

    if 'change_password' in request.form and pw_form.validate_on_submit():
        if check_password_hash(current_user.password_hash, pw_form.current_password.data):
            current_user.password_hash = generate_password_hash(pw_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
        else:
            flash('Current password is incorrect.', 'danger')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html', form=form, pw_form=pw_form)
