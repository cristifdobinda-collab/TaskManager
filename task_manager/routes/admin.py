from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.task import Task

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate yourself.', 'error')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ('user', 'manager', 'admin'):
        user.role = new_role
        db.session.commit()
        flash(f'Role for {user.username} changed to {new_role}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/settings')
@admin_required
def settings():
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_tasks': Task.query.count(),
    }
    return render_template('admin/settings.html', stats=stats)
