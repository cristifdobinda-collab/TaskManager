from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db
from models.task import Task
from models.team import Team
from models.user import User
from models.comment import Comment

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    now = datetime.utcnow()
    upcoming = now + timedelta(days=7)

    my_tasks = Task.query.filter(
        (Task.assignee_id == current_user.id) & (Task.status != 'done')
    ).order_by(Task.deadline.asc().nullslast()).all()

    upcoming_deadlines = Task.query.filter(
        Task.assignee_id == current_user.id,
        Task.status != 'done',
        Task.deadline.isnot(None),
        Task.deadline <= upcoming,
    ).order_by(Task.deadline.asc()).all()

    recent_comments = Comment.query.join(Task).filter(
        (Task.creator_id == current_user.id) | (Task.assignee_id == current_user.id)
    ).order_by(Comment.created_at.desc()).limit(10).all()

    stats = {
        'total': Task.query.filter(
            (Task.assignee_id == current_user.id) | (Task.creator_id == current_user.id)
        ).count(),
        'todo': Task.query.filter_by(assignee_id=current_user.id, status='todo').count(),
        'in_progress': Task.query.filter_by(assignee_id=current_user.id, status='in_progress').count(),
        'done': Task.query.filter_by(assignee_id=current_user.id, status='done').count(),
        'overdue': Task.query.filter(
            Task.assignee_id == current_user.id,
            Task.status != 'done',
            Task.deadline.isnot(None),
            Task.deadline < now,
        ).count(),
    }

    my_teams = current_user.teams

    return render_template('dashboard/index.html', my_tasks=my_tasks,
                           upcoming_deadlines=upcoming_deadlines,
                           recent_comments=recent_comments, stats=stats,
                           my_teams=my_teams)


@dashboard_bp.route('/overview')
@login_required
def overview():
    if current_user.role not in ('manager', 'admin'):
        return render_template('dashboard/index.html')

    now = datetime.utcnow()
    users = User.query.filter_by(is_active=True).all()
    teams = Team.query.all()

    workload = []
    for user in users:
        count = Task.query.filter_by(assignee_id=user.id).filter(Task.status != 'done').count()
        workload.append({'user': user, 'count': count})
    workload.sort(key=lambda x: x['count'], reverse=True)

    overdue_tasks = Task.query.filter(
        Task.status != 'done',
        Task.deadline.isnot(None),
        Task.deadline < now,
    ).order_by(Task.deadline.asc()).all()

    status_counts = {
        'todo': Task.query.filter_by(status='todo').count(),
        'in_progress': Task.query.filter_by(status='in_progress').count(),
        'review': Task.query.filter_by(status='review').count(),
        'done': Task.query.filter_by(status='done').count(),
    }

    return render_template('dashboard/overview.html', workload=workload,
                           overdue_tasks=overdue_tasks, status_counts=status_counts,
                           teams=teams)


@dashboard_bp.route('/analytics')
@login_required
def analytics():
    if current_user.role != 'admin':
        return render_template('dashboard/index.html')

    total_users = User.query.count()
    total_tasks = Task.query.count()
    total_comments = Comment.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_teams = Team.query.count()

    priority_counts = {
        'low': Task.query.filter_by(priority='low').count(),
        'medium': Task.query.filter_by(priority='medium').count(),
        'high': Task.query.filter_by(priority='high').count(),
        'critical': Task.query.filter_by(priority='critical').count(),
    }

    teams = Team.query.all()

    return render_template('dashboard/analytics.html',
                           total_users=total_users, total_tasks=total_tasks,
                           total_comments=total_comments, active_users=active_users,
                           total_teams=total_teams, priority_counts=priority_counts,
                           teams=teams)
