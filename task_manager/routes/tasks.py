import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from models import db
from models.task import Task, Tag
from models.team import Team
from models.comment import Comment
from models.user import User
from models.notification import Notification
from routes.notifications import notify_user

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
@login_required
def list_tasks():
    query = Task.query
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee = request.args.get('assignee')
    team = request.args.get('team')
    search = request.args.get('q', '').strip()

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assignee:
        query = query.filter_by(assignee_id=int(assignee))
    if team:
        query = query.filter_by(team_id=int(team))
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))

    tasks = query.order_by(Task.created_at.desc()).all()
    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    teams = Team.query.order_by(Team.name).all()
    return render_template('tasks/list.html', tasks=tasks, users=users, teams=teams,
                           current_status=status, current_priority=priority,
                           current_assignee=assignee, current_team=team,
                           search_query=search)


@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        assignee_id = request.form.get('assignee_id') or None
        team_id = request.form.get('team_id') or None
        deadline_str = request.form.get('deadline', '').strip()
        tags_str = request.form.get('tags', '').strip()

        if not title:
            flash('Title is required.', 'error')
            users = User.query.filter_by(is_active=True).order_by(User.username).all()
            teams = Team.query.order_by(Team.name).all()
            return render_template('tasks/create.html', users=users, teams=teams)

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                except ValueError:
                    pass

        task = Task(
            title=title,
            description=description,
            priority=priority,
            creator_id=current_user.id,
            assignee_id=int(assignee_id) if assignee_id else None,
            team_id=int(team_id) if team_id else None,
            deadline=deadline,
        )

        if tags_str:
            for tag_name in [t.strip() for t in tags_str.split(',') if t.strip()]:
                tag = Tag.query.filter_by(name=tag_name.lower()).first()
                if not tag:
                    tag = Tag(name=tag_name.lower())
                    db.session.add(tag)
                task.tags.append(tag)

        db.session.add(task)
        db.session.commit()

        if task.assignee_id and task.assignee_id != current_user.id:
            notify_user(
                task.assignee_id, 'assignment',
                f'{current_user.username} assigned you task: {task.title}',
                url_for('tasks.detail', task_id=task.id),
            )

        flash('Task created successfully.', 'success')
        return redirect(url_for('tasks.detail', task_id=task.id))

    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    teams = Team.query.order_by(Team.name).all()
    return render_template('tasks/create.html', users=users, teams=teams)


@tasks_bp.route('/<int:task_id>')
@login_required
def detail(task_id):
    task = Task.query.get_or_404(task_id)
    comments = Comment.query.filter_by(task_id=task_id, parent_id=None).order_by(Comment.created_at.asc()).all()
    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    return render_template('tasks/detail.html', task=task, comments=comments, users=users)


@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.creator_id != current_user.id and current_user.role not in ('manager', 'admin'):
        abort(403)

    if request.method == 'POST':
        task.title = request.form.get('title', '').strip() or task.title
        task.description = request.form.get('description', '').strip()
        task.priority = request.form.get('priority', task.priority)
        task.status = request.form.get('status', task.status)

        new_assignee_id = request.form.get('assignee_id') or None
        old_assignee_id = task.assignee_id
        task.assignee_id = int(new_assignee_id) if new_assignee_id else None

        team_id = request.form.get('team_id') or None
        task.team_id = int(team_id) if team_id else None

        deadline_str = request.form.get('deadline', '').strip()
        if deadline_str:
            try:
                task.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                except ValueError:
                    pass
        else:
            task.deadline = None

        tags_str = request.form.get('tags', '').strip()
        task.tags.clear()
        if tags_str:
            for tag_name in [t.strip() for t in tags_str.split(',') if t.strip()]:
                tag = Tag.query.filter_by(name=tag_name.lower()).first()
                if not tag:
                    tag = Tag(name=tag_name.lower())
                    db.session.add(tag)
                task.tags.append(tag)

        db.session.commit()

        if task.assignee_id and task.assignee_id != old_assignee_id and task.assignee_id != current_user.id:
            notify_user(
                task.assignee_id, 'assignment',
                f'{current_user.username} assigned you task: {task.title}',
                url_for('tasks.detail', task_id=task.id),
            )

        flash('Task updated.', 'success')
        return redirect(url_for('tasks.detail', task_id=task.id))

    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    teams = Team.query.order_by(Team.name).all()
    return render_template('tasks/edit.html', task=task, users=users, teams=teams)


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.creator_id != current_user.id and current_user.role != 'admin':
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/<int:task_id>/status', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_status = data.get('status')
    if new_status in ('todo', 'in_progress', 'review', 'done'):
        task.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status, 'label': task.status_label})
    return jsonify({'success': False}), 400


@tasks_bp.route('/<int:task_id>/comment', methods=['POST'])
@login_required
def add_comment(task_id):
    task = Task.query.get_or_404(task_id)
    content = request.form.get('content', '').strip()
    parent_id = request.form.get('parent_id') or None

    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('tasks.detail', task_id=task_id))

    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=current_user.id,
        parent_id=int(parent_id) if parent_id else None,
    )
    db.session.add(comment)
    db.session.commit()

    # Notify task creator and assignee
    notify_targets = set()
    if task.creator_id != current_user.id:
        notify_targets.add(task.creator_id)
    if task.assignee_id and task.assignee_id != current_user.id:
        notify_targets.add(task.assignee_id)

    # Parse @mentions (supports usernames with dots, hyphens, underscores)
    mentions = re.findall(r'@([\w.\-]+)', content)
    for username in mentions:
        mentioned_user = User.query.filter_by(username=username).first()
        if mentioned_user and mentioned_user.id != current_user.id:
            notify_targets.add(mentioned_user.id)

    for uid in notify_targets:
        notify_user(
            uid, 'comment',
            f'{current_user.username} mentioned you on: {task.title}' if uid not in {task.creator_id, task.assignee_id}
            else f'{current_user.username} commented on: {task.title}',
            url_for('tasks.detail', task_id=task.id),
        )

    flash('Comment added.', 'success')
    return redirect(url_for('tasks.detail', task_id=task_id))


@tasks_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id and current_user.role != 'admin':
        abort(403)
    task_id = comment.task_id
    db.session.delete(comment)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    flash('Comment deleted.', 'success')
    return redirect(url_for('tasks.detail', task_id=task_id))
