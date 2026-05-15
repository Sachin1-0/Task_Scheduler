from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models import Category
from app.forms import CategoryForm

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
@login_required
def list_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories/list.html', title='My Categories', categories=categories)

@categories_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('categories.list_categories'))
    return render_template('categories/create_edit.html', title='New Category', form=form, legend='New Category')

@categories_bp.route('/category/<int:category_id>/update', methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        flash('You cannot edit this category.', 'danger')
        return redirect(url_for('categories.list_categories'))
    
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('categories.list_categories'))
    elif request.method == 'GET':
        form.name.data = category.name
    return render_template('categories/create_edit.html', title='Update Category', form=form, legend='Update Category')

@categories_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        flash('You cannot delete this category.', 'danger')
        return redirect(url_for('categories.list_categories'))
    
    # Optional: Handle tasks associated with this category (e.g., set them to None)
    for task in category.tasks:
        task.category_id = None
        
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('categories.list_categories'))
