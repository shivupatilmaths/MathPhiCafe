from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from . import auth_bp
from ...models import AdminUser, Student
from ...forms import LoginForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    form = LoginForm()
    role = request.args.get('role', 'student')

    if form.validate_on_submit():
        role = request.form.get('role', 'student')
        if role == 'admin':
            user = AdminUser.query.filter_by(username=form.username.data).first()
        else:
            user = Student.query.filter_by(student_id=form.username.data, is_active=True).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('auth/login.html', form=form, role=role)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('public.home'))
