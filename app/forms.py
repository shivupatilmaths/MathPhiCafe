from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField,
    IntegerField, FloatField, BooleanField, DateField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, Optional, NumberRange, ValidationError
)


# ---------- Auth ----------
class LoginForm(FlaskForm):
    username = StringField('Username / Student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# ---------- Admin: Student ----------
class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    grade = SelectField('Grade', choices=[
        (9, 'Grade 9'), (10, 'Grade 10'), (11, 'Grade 11'), (12, 'Grade 12')
    ], coerce=int, validators=[DataRequired()])
    parent_name = StringField('Parent Name', validators=[Optional(), Length(max=120)])
    parent_phone = StringField('Parent Phone', validators=[Optional(), Length(max=15)])
    address = TextAreaField('Address', validators=[Optional()])
    date_of_birth = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Save Student')


# ---------- Admin: Batch ----------
class BatchForm(FlaskForm):
    name = StringField('Batch Name', validators=[DataRequired(), Length(max=100)])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    grade = SelectField('Grade', choices=[
        (9, 'Grade 9'), (10, 'Grade 10'), (11, 'Grade 11'), (12, 'Grade 12')
    ], coerce=int, validators=[DataRequired()])
    faculty_id = SelectField('Faculty', coerce=int, validators=[Optional()])
    schedule = StringField('Schedule', validators=[Optional(), Length(max=200)])
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    max_students = IntegerField('Max Students', default=30, validators=[Optional(), NumberRange(min=1)])
    submit = SubmitField('Save Batch')


# ---------- Admin: Result ----------
class ResultForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    exam_name = StringField('Exam Name', validators=[DataRequired(), Length(max=100)])
    exam_date = DateField('Exam Date', validators=[DataRequired()], format='%Y-%m-%d')
    marks_obtained = FloatField('Marks Obtained', validators=[DataRequired(), NumberRange(min=0)])
    total_marks = FloatField('Total Marks', validators=[DataRequired(), NumberRange(min=1)])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Save Result')


# ---------- Admin: Announcement ----------
class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('general', 'General'), ('exam', 'Exam'), ('holiday', 'Holiday'), ('event', 'Event')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')
    ], default='normal')
    target_grade = SelectField('Target Grade', choices=[
        (0, 'All Grades'), (9, 'Grade 9'), (10, 'Grade 10'), (11, 'Grade 11'), (12, 'Grade 12')
    ], coerce=int)
    submit = SubmitField('Save Announcement')


# ---------- Admin: Faculty ----------
class FacultyForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    qualification = StringField('Qualification', validators=[Optional(), Length(max=200)])
    experience = StringField('Experience', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional()])
    specialization = StringField('Specialization', validators=[Optional(), Length(max=200)])
    photo = FileField('Photo', validators=[
        Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Save Faculty')


# ---------- Admin: Gallery ----------
class GalleryUploadForm(FlaskForm):
    images = FileField('Upload Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    caption = StringField('Caption', validators=[Optional(), Length(max=200)])
    category = SelectField('Category', choices=[
        ('general', 'General'), ('classroom', 'Classroom'),
        ('events', 'Events'), ('achievements', 'Achievements'), ('campus', 'Campus')
    ])
    submit = SubmitField('Upload')


# ---------- Admin: Note ----------
class NoteUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    grade = SelectField('Grade', choices=[
        (9, 'Grade 9'), (10, 'Grade 10'), (11, 'Grade 11'), (12, 'Grade 12')
    ], coerce=int, validators=[DataRequired()])
    chapter = StringField('Chapter', validators=[Optional(), Length(max=100)])
    file = FileField('PDF File', validators=[
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    submit = SubmitField('Upload Note')


# ---------- Admin: Testimonial ----------
class TestimonialForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=120)])
    content = TextAreaField('Testimonial', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[
        (5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')
    ], coerce=int)
    grade = StringField('Grade/Year', validators=[Optional(), Length(max=20)])
    is_featured = BooleanField('Featured on Home Page')
    submit = SubmitField('Save Testimonial')


# ---------- Public: Contact ----------
class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Your Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


# ---------- Student: Profile ----------
class ProfileForm(FlaskForm):
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    address = TextAreaField('Address', validators=[Optional()])
    avatar = FileField('Profile Photo', validators=[
        Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Passwords do not match.')
