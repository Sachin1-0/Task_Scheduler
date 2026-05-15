from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Task, User
from app.forms import UpdateProfileForm, ChangePasswordForm, UpdatePhotoForm
from app import db
from app.utils import save_picture
from datetime import date

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'Completed'])
    pending_tasks = len([t for t in tasks if t.status != 'Completed'])
    today = date.today()
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < today and t.status != 'Completed'])
    today_tasks = len([t for t in tasks if t.due_date == today])

    return render_template('main/dashboard.html', title='Dashboard', 
                           total_tasks=total_tasks, completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks, overdue_tasks=overdue_tasks,
                           today_tasks=today_tasks)

@main_bp.route('/profile')
@login_required
def profile():
    profile_form = UpdateProfileForm()
    password_form = ChangePasswordForm()
    photo_form = UpdatePhotoForm()
    
    profile_form.username.data = current_user.username
    profile_form.email.data = current_user.email
    
    image_file = url_for('static', filename='uploads/' + current_user.profile_image)
    return render_template('main/profile.html', title='Profile', image_file=image_file, 
                           profile_form=profile_form, password_form=password_form, photo_form=photo_form)

@main_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
    else:
        for error in profile_form.errors.values():
            flash(error[0], 'danger')
    return redirect(url_for('main.profile'))

@main_bp.route('/profile/password', methods=['POST'])
@login_required
def update_password():
    password_form = ChangePasswordForm()
    if password_form.validate_on_submit():
        if current_user.check_password(password_form.old_password.data):
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
        else:
            flash('Incorrect current password.', 'danger')
    else:
        for error in password_form.errors.values():
            flash(error[0], 'danger')
    return redirect(url_for('main.profile'))

@main_bp.route('/profile/photo', methods=['POST'])
@login_required
def update_photo():
    photo_form = UpdatePhotoForm()
    if photo_form.validate_on_submit():
        if photo_form.picture.data:
            picture_file = save_picture(photo_form.picture.data)
            current_user.profile_image = picture_file
            db.session.commit()
            flash('Your profile picture has been updated!', 'success')
    else:
        for error in photo_form.errors.values():
            flash(error[0], 'danger')
    return redirect(url_for('main.profile'))

@main_bp.route('/calendar')
@login_required
def calendar():
    return render_template('main/calendar.html', title='Calendar')

@main_bp.route('/toggle_theme', methods=['POST'])
@login_required
def toggle_theme():
    current_user.dark_mode = not current_user.dark_mode
    db.session.commit()
    return {'status': 'success', 'dark_mode': current_user.dark_mode}
