import csv
import io
from flask import Blueprint, render_template, url_for, flash, redirect, request, Response
from flask_login import current_user, login_required
from app import db
from app.models import Task, Category
from app.forms import TaskForm
from app.utils import save_attachment
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def list_tasks():
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    search_query = request.args.get('search')
    
    query = Task.query.filter_by(user_id=current_user.id, is_deleted=False)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if search_query:
        query = query.filter(Task.title.contains(search_query) | Task.description.contains(search_query))
        
    tasks = query.order_by(Task.due_date.asc()).all()
    return render_template('tasks/list.html', title='My Tasks', tasks=tasks, now=datetime.now(), datetime=datetime)

@tasks_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    # Populate categories
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(0, 'None')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        attachment_file = None
        if form.attachment.data:
            attachment_file = save_attachment(form.attachment.data)
        
        task = Task(title=form.title.data,
                    description=form.description.data,
                    due_date=form.due_date.data,
                    due_time=form.due_time.data,
                    priority=form.priority.data,
                    status=form.status.data,
                    recurrence=form.recurrence.data,
                    attachment=attachment_file,
                    user_id=current_user.id,
                    category_id=form.category_id.data if form.category_id.data != 0 else None)
        db.session.add(task)
        db.session.commit()
        flash('Task has been created!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/create_edit.html', title='New Task', form=form, legend='New Task')

@tasks_bp.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        flash('You cannot edit this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
        
    form = TaskForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(0, 'None')] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.due_time = form.due_time.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.recurrence = form.recurrence.data
        task.category_id = form.category_id.data if form.category_id.data != 0 else None
        if form.attachment.data:
            task.attachment = save_attachment(form.attachment.data)
        db.session.commit()
        flash('Task has been updated!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.due_date.data = task.due_date
        form.due_time.data = task.due_time
        form.priority.data = task.priority
        form.status.data = task.status
        form.recurrence.data = task.recurrence
        form.category_id.data = task.category_id if task.category_id else 0
    return render_template('tasks/create_edit.html', title='Update Task', form=form, legend='Update Task')

@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        flash('You cannot delete this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    task.is_deleted = True
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/tasks/export/csv')
@login_required
def export_csv():
    tasks = Task.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Title', 'Description', 'Due Date', 'Due Time', 'Priority', 'Status', 'Category'])
    
    for t in tasks:
        cat_name = t.category.name if t.category else 'None'
        cw.writerow([t.title, t.description, t.due_date, t.due_time, t.priority, t.status, cat_name])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=tasks.csv"}
    )

@tasks_bp.route('/api/tasks/pending')
@login_required
def api_pending_tasks():
    tasks = Task.query.filter(Task.user_id == current_user.id, Task.status != 'Completed', Task.is_deleted == False).all()
    tasks_data = []
    for t in tasks:
        tasks_data.append({
            'id': t.id,
            'title': t.title,
            'due_date': t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            'due_time': t.due_time.strftime('%H:%M:%S') if t.due_time else None
        })
    return {'tasks': tasks_data}

@tasks_bp.route('/api/tasks/calendar')
@login_required
def api_calendar_tasks():
    tasks = Task.query.filter(Task.user_id == current_user.id, Task.is_deleted == False).all()
    events = []
    for t in tasks:
        if t.due_date:
            start_str = t.due_date.strftime('%Y-%m-%d')
            if t.due_time:
                start_str += 'T' + t.due_time.strftime('%H:%M:%S')
            
            # Color code based on status
            bg_color = '#6c757d' # Pending (Secondary)
            if t.status == 'Completed':
                bg_color = '#198754' # Success
            elif t.status == 'In Progress':
                bg_color = '#0d6efd' # Primary
                
            events.append({
                'title': t.title,
                'start': start_str,
                'url': url_for('tasks.update_task', task_id=t.id),
                'backgroundColor': bg_color,
                'borderColor': bg_color
            })
    return events
