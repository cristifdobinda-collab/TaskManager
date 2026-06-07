from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.comment import Comment
from models.task import Task
from models.notification import Notification

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/')
@login_required
def view():
    # Task stats
    total_assigned = current_user.tasks_assigned.count()
    total_created = current_user.tasks_created.count()
    completed = current_user.tasks_assigned.filter_by(status='done').count()
    in_progress = current_user.tasks_assigned.filter_by(status='in_progress').count()
    todo = current_user.tasks_assigned.filter_by(status='todo').count()
    overdue = current_user.tasks_assigned.filter(
        Task.status != 'done',
        Task.deadline.isnot(None),
        Task.deadline < datetime.utcnow(),
    ).count()
    completion_rate = round((completed / total_assigned * 100) if total_assigned > 0 else 0)

    # Priority breakdown
    priority_stats = {}
    for p in ('low', 'medium', 'high', 'critical'):
        priority_stats[p] = current_user.tasks_assigned.filter_by(priority=p).count()

    recent_tasks = Task.query.filter(
        (Task.creator_id == current_user.id) | (Task.assignee_id == current_user.id)
    ).order_by(Task.updated_at.desc()).limit(10).all()

    recent_comments = Comment.query.filter_by(user_id=current_user.id).order_by(
        Comment.created_at.desc()
    ).limit(10).all()

    teams = current_user.teams
    total_comments = current_user.comments.count()

    return render_template('profile/view.html',
                           recent_tasks=recent_tasks, recent_comments=recent_comments,
                           total_assigned=total_assigned, total_created=total_created,
                           completed=completed, in_progress=in_progress, todo=todo,
                           overdue=overdue, completion_rate=completion_rate,
                           priority_stats=priority_stats, teams=teams,
                           total_comments=total_comments)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email and '@' in email:
            current_user.email = email

        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.job_title = request.form.get('job_title', '').strip()
        current_user.department = request.form.get('department', '').strip()
        current_user.bio = request.form.get('bio', '').strip()

        current_user.notify_assignment = request.form.get('notify_assignment') == 'on'
        current_user.notify_comments = request.form.get('notify_comments') == 'on'
        current_user.notify_deadlines = request.form.get('notify_deadlines') == 'on'

        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('profile.view'))

    return render_template('profile/edit.html')


@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')

    if not current_user.check_password(current_pw):
        flash('Current password is incorrect.', 'error')
    elif len(new_pw) < 6:
        flash('New password must be at least 6 characters.', 'error')
    elif new_pw != confirm_pw:
        flash('Passwords do not match.', 'error')
    else:
        current_user.set_password(new_pw)
        db.session.commit()
        flash('Password changed successfully.', 'success')

    return redirect(url_for('profile.edit'))
