import os
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from werkzeug.security import generate_password_hash
from . import admin_bp
from ...extensions import db
from ...models import (
    AdminUser, Student, Subject, Faculty, Batch, BatchEnrollment,
    Result, Announcement, GalleryImage, Note, Testimonial, ContactMessage, SiteSetting
)
from ...forms import (
    StudentForm, BatchForm, ResultForm, AnnouncementForm,
    FacultyForm, GalleryUploadForm, NoteUploadForm, TestimonialForm
)
from ...utils import (
    admin_required, generate_student_id, generate_random_password,
    calculate_grade, save_image, save_file, allowed_file, create_thumbnail
)


# ==================== Dashboard ====================

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'students': Student.query.filter_by(is_active=True).count(),
        'batches': Batch.query.filter_by(is_active=True).count(),
        'messages': ContactMessage.query.filter_by(is_read=False).count(),
        'announcements': Announcement.query.filter_by(is_active=True).count(),
    }
    recent_students = Student.query.filter_by(is_active=True).order_by(
        Student.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_students=recent_students,
                           recent_messages=recent_messages)


# ==================== Students ====================

@admin_bp.route('/students')
@login_required
@admin_required
def students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    grade_filter = request.args.get('grade', 0, type=int)

    query = Student.query.filter_by(is_active=True)
    if search:
        query = query.filter(
            db.or_(
                Student.full_name.ilike(f'%{search}%'),
                Student.student_id.ilike(f'%{search}%')
            )
        )
    if grade_filter:
        query = query.filter_by(grade=grade_filter)

    students = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False)
    return render_template('admin/students.html', students=students,
                           search=search, grade_filter=grade_filter)


@admin_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    form = StudentForm()
    generated_password = None
    generated_id = None

    if form.validate_on_submit():
        password = generate_random_password()
        student_id = generate_student_id()
        student = Student(
            student_id=student_id,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            grade=form.grade.data,
            parent_name=form.parent_name.data,
            parent_phone=form.parent_phone.data,
            address=form.address.data,
            date_of_birth=form.date_of_birth.data,
            password_hash=generate_password_hash(password)
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Student added! ID: {student_id} | Password: {password} (share this with the student)', 'success')
        return redirect(url_for('admin.students'))

    return render_template('admin/student_form.html', form=form, editing=False,
                           generated_password=generated_password,
                           generated_id=generated_id)


@admin_bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        student.full_name = form.full_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.grade = form.grade.data
        student.parent_name = form.parent_name.data
        student.parent_phone = form.parent_phone.data
        student.address = form.address.data
        student.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('admin.students'))

    return render_template('admin/student_form.html', form=form, editing=True, student=student)


@admin_bp.route('/students/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    student.is_active = False
    db.session.commit()
    flash('Student deactivated.', 'info')
    return redirect(url_for('admin.students'))


@admin_bp.route('/students/<int:id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_student_password(id):
    student = Student.query.get_or_404(id)
    password = generate_random_password()
    student.password_hash = generate_password_hash(password)
    db.session.commit()
    flash(f'Password reset for {student.full_name}. New password: {password}', 'success')
    return redirect(url_for('admin.edit_student', id=id))


# ==================== Batches ====================

@admin_bp.route('/batches')
@login_required
@admin_required
def batches():
    batches = Batch.query.filter_by(is_active=True).order_by(Batch.created_at.desc()).all()
    return render_template('admin/batches.html', batches=batches)


@admin_bp.route('/batches/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_batch():
    form = BatchForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.filter_by(is_active=True).all()]
    form.faculty_id.choices = [(0, '-- Select Faculty --')] + [
        (f.id, f.full_name) for f in Faculty.query.filter_by(is_active=True).all()
    ]
    if form.validate_on_submit():
        batch = Batch(
            name=form.name.data,
            subject_id=form.subject_id.data,
            grade=form.grade.data,
            faculty_id=form.faculty_id.data if form.faculty_id.data else None,
            schedule=form.schedule.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            max_students=form.max_students.data
        )
        db.session.add(batch)
        db.session.commit()
        flash('Batch created successfully!', 'success')
        return redirect(url_for('admin.batches'))
    return render_template('admin/batch_form.html', form=form, editing=False)


@admin_bp.route('/batches/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_batch(id):
    batch = Batch.query.get_or_404(id)
    form = BatchForm(obj=batch)
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.filter_by(is_active=True).all()]
    form.faculty_id.choices = [(0, '-- Select Faculty --')] + [
        (f.id, f.full_name) for f in Faculty.query.filter_by(is_active=True).all()
    ]
    if form.validate_on_submit():
        batch.name = form.name.data
        batch.subject_id = form.subject_id.data
        batch.grade = form.grade.data
        batch.faculty_id = form.faculty_id.data if form.faculty_id.data else None
        batch.schedule = form.schedule.data
        batch.start_date = form.start_date.data
        batch.end_date = form.end_date.data
        batch.max_students = form.max_students.data
        db.session.commit()
        flash('Batch updated!', 'success')
        return redirect(url_for('admin.batches'))
    return render_template('admin/batch_form.html', form=form, editing=True, batch=batch)


@admin_bp.route('/batches/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_batch(id):
    batch = Batch.query.get_or_404(id)
    batch.is_active = False
    db.session.commit()
    flash('Batch deactivated.', 'info')
    return redirect(url_for('admin.batches'))


@admin_bp.route('/batches/<int:id>/enroll', methods=['GET', 'POST'])
@login_required
@admin_required
def enroll_students(id):
    batch = Batch.query.get_or_404(id)
    enrolled_ids = [e.student_id for e in batch.enrollments.all()]
    available = Student.query.filter_by(
        is_active=True, grade=batch.grade
    ).filter(~Student.id.in_(enrolled_ids) if enrolled_ids else True).all()

    if request.method == 'POST':
        student_ids = request.form.getlist('student_ids', type=int)
        for sid in student_ids:
            enrollment = BatchEnrollment(student_id=sid, batch_id=batch.id)
            db.session.add(enrollment)
        db.session.commit()
        flash(f'{len(student_ids)} student(s) enrolled!', 'success')
        return redirect(url_for('admin.batches'))

    enrolled = Student.query.filter(Student.id.in_(enrolled_ids)).all() if enrolled_ids else []
    return render_template('admin/enroll.html', batch=batch,
                           available=available, enrolled=enrolled)


# ==================== Results ====================

@admin_bp.route('/results')
@login_required
@admin_required
def results():
    page = request.args.get('page', 1, type=int)
    results = Result.query.order_by(Result.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/results.html', results=results)


@admin_bp.route('/results/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_result():
    form = ResultForm()
    form.student_id.choices = [(s.id, f'{s.student_id} - {s.full_name}')
                               for s in Student.query.filter_by(is_active=True).all()]
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        percentage = (form.marks_obtained.data / form.total_marks.data) * 100
        result = Result(
            student_id=form.student_id.data,
            subject_id=form.subject_id.data,
            exam_name=form.exam_name.data,
            exam_date=form.exam_date.data,
            marks_obtained=form.marks_obtained.data,
            total_marks=form.total_marks.data,
            grade_letter=calculate_grade(percentage),
            remarks=form.remarks.data
        )
        db.session.add(result)
        db.session.commit()
        flash('Result added!', 'success')
        return redirect(url_for('admin.results'))
    return render_template('admin/result_form.html', form=form, editing=False)


@admin_bp.route('/results/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_result(id):
    result = Result.query.get_or_404(id)
    form = ResultForm(obj=result)
    form.student_id.choices = [(s.id, f'{s.student_id} - {s.full_name}')
                               for s in Student.query.filter_by(is_active=True).all()]
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        result.student_id = form.student_id.data
        result.subject_id = form.subject_id.data
        result.exam_name = form.exam_name.data
        result.exam_date = form.exam_date.data
        result.marks_obtained = form.marks_obtained.data
        result.total_marks = form.total_marks.data
        percentage = (form.marks_obtained.data / form.total_marks.data) * 100
        result.grade_letter = calculate_grade(percentage)
        result.remarks = form.remarks.data
        db.session.commit()
        flash('Result updated!', 'success')
        return redirect(url_for('admin.results'))
    return render_template('admin/result_form.html', form=form, editing=True, result=result)


@admin_bp.route('/results/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_result(id):
    result = Result.query.get_or_404(id)
    db.session.delete(result)
    db.session.commit()
    flash('Result deleted.', 'info')
    return redirect(url_for('admin.results'))


# ==================== Announcements ====================

@admin_bp.route('/announcements')
@login_required
@admin_required
def announcements():
    items = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=items)


@admin_bp.route('/announcements/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        ann = Announcement(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            priority=form.priority.data,
            target_grade=form.target_grade.data if form.target_grade.data else None
        )
        db.session.add(ann)
        db.session.commit()
        flash('Announcement created!', 'success')
        return redirect(url_for('admin.announcements'))
    return render_template('admin/announcement_form.html', form=form, editing=False)


@admin_bp.route('/announcements/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(id):
    ann = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=ann)
    if ann.target_grade is None:
        form.target_grade.data = 0
    if form.validate_on_submit():
        ann.title = form.title.data
        ann.content = form.content.data
        ann.category = form.category.data
        ann.priority = form.priority.data
        ann.target_grade = form.target_grade.data if form.target_grade.data else None
        db.session.commit()
        flash('Announcement updated!', 'success')
        return redirect(url_for('admin.announcements'))
    return render_template('admin/announcement_form.html', form=form, editing=True, announcement=ann)


@admin_bp.route('/announcements/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_announcement(id):
    ann = Announcement.query.get_or_404(id)
    db.session.delete(ann)
    db.session.commit()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('admin.announcements'))


# ==================== Gallery ====================

@admin_bp.route('/gallery')
@login_required
@admin_required
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.sort_order, GalleryImage.uploaded_at.desc()).all()
    form = GalleryUploadForm()
    return render_template('admin/gallery_manage.html', images=images, form=form)


@admin_bp.route('/gallery/upload', methods=['POST'])
@login_required
@admin_required
def upload_gallery():
    form = GalleryUploadForm()
    if form.images.data:
        file = form.images.data
        if allowed_file(file.filename, current_app.config['ALLOWED_IMAGE_EXTENSIONS']):
            filename = save_image(file, current_app.config['GALLERY_FOLDER'])
            source_path = os.path.join(current_app.config['GALLERY_FOLDER'], filename)
            thumb = create_thumbnail(source_path, current_app.config['THUMBNAILS_FOLDER'])
            image = GalleryImage(
                filename=filename,
                thumbnail=thumb,
                caption=form.caption.data,
                category=form.category.data
            )
            db.session.add(image)
            db.session.commit()
            flash('Image uploaded!', 'success')
        else:
            flash('Invalid file type.', 'danger')
    return redirect(url_for('admin.gallery'))


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_gallery_image(id):
    image = GalleryImage.query.get_or_404(id)
    try:
        path = os.path.join(current_app.config['GALLERY_FOLDER'], image.filename)
        if os.path.exists(path):
            os.remove(path)
        if image.thumbnail:
            thumb_path = os.path.join(current_app.config['THUMBNAILS_FOLDER'], image.thumbnail)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
    except OSError:
        pass
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted.', 'info')
    return redirect(url_for('admin.gallery'))


# ==================== Faculty ====================

@admin_bp.route('/faculty')
@login_required
@admin_required
def faculty():
    faculty = Faculty.query.order_by(Faculty.sort_order).all()
    return render_template('admin/faculty_manage.html', faculty=faculty)


@admin_bp.route('/faculty/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_faculty():
    form = FacultyForm()
    if form.validate_on_submit():
        photo = 'default-avatar.png'
        if form.photo.data:
            photo = save_image(form.photo.data, current_app.config['AVATARS_FOLDER'])
        f = Faculty(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            qualification=form.qualification.data,
            experience=form.experience.data,
            bio=form.bio.data,
            specialization=form.specialization.data,
            photo=photo
        )
        db.session.add(f)
        db.session.commit()
        flash('Faculty member added!', 'success')
        return redirect(url_for('admin.faculty'))
    return render_template('admin/faculty_form.html', form=form, editing=False)


@admin_bp.route('/faculty/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_faculty(id):
    fac = Faculty.query.get_or_404(id)
    form = FacultyForm(obj=fac)
    if form.validate_on_submit():
        fac.full_name = form.full_name.data
        fac.email = form.email.data
        fac.phone = form.phone.data
        fac.qualification = form.qualification.data
        fac.experience = form.experience.data
        fac.bio = form.bio.data
        fac.specialization = form.specialization.data
        if form.photo.data:
            fac.photo = save_image(form.photo.data, current_app.config['AVATARS_FOLDER'])
        db.session.commit()
        flash('Faculty updated!', 'success')
        return redirect(url_for('admin.faculty'))
    return render_template('admin/faculty_form.html', form=form, editing=True, faculty_member=fac)


@admin_bp.route('/faculty/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_faculty(id):
    fac = Faculty.query.get_or_404(id)
    fac.is_active = False
    db.session.commit()
    flash('Faculty deactivated.', 'info')
    return redirect(url_for('admin.faculty'))


# ==================== Testimonials ====================

@admin_bp.route('/testimonials')
@login_required
@admin_required
def testimonials():
    items = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials_manage.html', testimonials=items)


@admin_bp.route('/testimonials/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        t = Testimonial(
            student_name=form.student_name.data,
            content=form.content.data,
            rating=form.rating.data,
            grade=form.grade.data,
            is_featured=form.is_featured.data
        )
        db.session.add(t)
        db.session.commit()
        flash('Testimonial added!', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, editing=False)


@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=t)
    if form.validate_on_submit():
        t.student_name = form.student_name.data
        t.content = form.content.data
        t.rating = form.rating.data
        t.grade = form.grade.data
        t.is_featured = form.is_featured.data
        db.session.commit()
        flash('Testimonial updated!', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, editing=True, testimonial=t)


@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('Testimonial deleted.', 'info')
    return redirect(url_for('admin.testimonials'))


# ==================== Notes ====================

@admin_bp.route('/notes')
@login_required
@admin_required
def notes():
    items = Note.query.filter_by(is_active=True).order_by(Note.uploaded_at.desc()).all()
    return render_template('admin/notes.html', notes=items)


@admin_bp.route('/notes/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_note():
    form = NoteUploadForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.filter_by(is_active=True).all()]
    if form.validate_on_submit():
        if form.file.data:
            filename, file_size = save_file(form.file.data, current_app.config['NOTES_FOLDER'])
            note = Note(
                title=form.title.data,
                subject_id=form.subject_id.data,
                grade=form.grade.data,
                chapter=form.chapter.data,
                filename=filename,
                file_size=file_size
            )
            db.session.add(note)
            db.session.commit()
            flash('Note uploaded!', 'success')
            return redirect(url_for('admin.notes'))
        flash('Please select a PDF file.', 'warning')
    return render_template('admin/note_form.html', form=form, editing=False)


@admin_bp.route('/notes/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        path = os.path.join(current_app.config['NOTES_FOLDER'], note.filename)
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
    note.is_active = False
    db.session.commit()
    flash('Note removed.', 'info')
    return redirect(url_for('admin.notes'))


# ==================== Messages ====================

@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=items)


@admin_bp.route('/messages/<int:id>')
@login_required
@admin_required
def view_message(id):
    msg = ContactMessage.query.get_or_404(id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
    return render_template('admin/message_detail.html', message=msg)


# ==================== Settings ====================

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    if request.method == 'POST':
        keys = ['site_name', 'tagline', 'phone', 'email', 'address',
                'about_text', 'google_maps_embed',
                'social_facebook', 'social_instagram', 'social_youtube']
        for key in keys:
            value = request.form.get(key, '')
            setting = SiteSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                db.session.add(SiteSetting(key=key, value=value))
        db.session.commit()
        flash('Settings saved!', 'success')
        return redirect(url_for('admin.settings'))

    settings = {}
    for s in SiteSetting.query.all():
        settings[s.key] = s.value
    return render_template('admin/settings.html', settings=settings)
