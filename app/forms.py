from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional
from flask_login import current_user
from app.models import User, Category

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20), 
                                       Regexp('^[A-Za-z0-9_]+$', message="Username must contain only letters, numbers, or underscore.")])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=64),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*\d)', message="Password must contain at least one number."),
        Regexp(r'(?=.*[@$!%*?&_\-])', message="Password must contain at least one special character.")
    ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20),
                                       Regexp('^[A-Za-z0-9_]+$', message="Username must contain only letters, numbers, or underscore.")])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update Details')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, max=64),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*\d)', message="Password must contain at least one number."),
        Regexp(r'(?=.*[@$!%*?&_\-])', message="Password must contain at least one special character.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class UpdatePhotoForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG, JPEG, and PNG are allowed!')])
    submit = SubmitField('Upload')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    due_time = TimeField('Due Time', format='%H:%M', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    recurrence = SelectField('Recurrence', choices=[('None', 'None'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], default='None')
    attachment = FileField('Attachment', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'])])
    submit = SubmitField('Save Task')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=64),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*\d)', message="Password must contain at least one number."),
        Regexp(r'(?=.*[@$!%*?&_\-])', message="Password must contain at least one special character.")
    ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Save Category')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data, user_id=current_user.id).first()
        if category:
            raise ValidationError('You already have a category with that name. Please choose a different one.')
