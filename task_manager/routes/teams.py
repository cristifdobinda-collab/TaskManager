from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db
from models.team import Team
from models.task import Task
from models.user import User, team_members

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')


@teams_bp.route('/')
@login_required
def list_teams():
    teams = Team.query.order_by(Team.name).all()
    return render_template('teams/list.html', teams=teams)


@teams_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role not in ('manager', 'admin'):
        abort(403)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#2563eb').strip()
        lead_id = request.form.get('lead_id') or None

        if not name:
            flash('Team name is required.', 'error')
            users = User.query.filter_by(is_active=True).order_by(User.username).all()
            return render_template('teams/create.html', users=users)

        if Team.query.filter_by(name=name).first():
            flash('A team with that name already exists.', 'error')
            users = User.query.filter_by(is_active=True).order_by(User.username).all()
            return render_template('teams/create.html', users=users)

        team = Team(
            name=name,
            description=description,
            color=color,
            lead_id=int(lead_id) if lead_id else None,
        )
        db.session.add(team)
        db.session.flush()

        # Add lead as member automatically
        if lead_id:
            lead = db.session.get(User, int(lead_id))
            if lead and lead not in team.members.all():
                team.members.append(lead)

        # Add selected members
        member_ids = request.form.getlist('member_ids')
        for mid in member_ids:
            user = db.session.get(User, int(mid))
            if user and user not in team.members.all():
                team.members.append(user)

        db.session.commit()
        flash(f'Team "{name}" created.', 'success')
        return redirect(url_for('teams.detail', team_id=team.id))

    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    return render_template('teams/create.html', users=users)


@teams_bp.route('/<int:team_id>')
@login_required
def detail(team_id):
    team = Team.query.get_or_404(team_id)
    members = team.members.all()
    tasks = team.tasks.filter(Task.status != 'done').order_by(Task.created_at.desc()).all()
    completed_tasks = team.tasks.filter_by(status='done').count()
    total_tasks = team.tasks.count()
    all_users = User.query.filter_by(is_active=True).order_by(User.username).all()
    return render_template('teams/detail.html', team=team, members=members,
                           tasks=tasks, completed_tasks=completed_tasks,
                           total_tasks=total_tasks, all_users=all_users)


@teams_bp.route('/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(team_id):
    team = Team.query.get_or_404(team_id)
    if current_user.role not in ('manager', 'admin') and current_user.id != team.lead_id:
        abort(403)

    if request.method == 'POST':
        team.name = request.form.get('name', '').strip() or team.name
        team.description = request.form.get('description', '').strip()
        team.color = request.form.get('color', team.color).strip()
        lead_id = request.form.get('lead_id') or None
        team.lead_id = int(lead_id) if lead_id else None

        db.session.commit()
        flash('Team updated.', 'success')
        return redirect(url_for('teams.detail', team_id=team.id))

    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    return render_template('teams/edit.html', team=team, users=users)


@teams_bp.route('/<int:team_id>/add-member', methods=['POST'])
@login_required
def add_member(team_id):
    team = Team.query.get_or_404(team_id)
    if current_user.role not in ('manager', 'admin') and current_user.id != team.lead_id:
        abort(403)

    user_id = request.form.get('user_id')
    if user_id:
        user = db.session.get(User, int(user_id))
        if user and user not in team.members.all():
            team.members.append(user)
            db.session.commit()
            flash(f'{user.username} added to team.', 'success')
        else:
            flash('User is already a member.', 'info')

    return redirect(url_for('teams.detail', team_id=team.id))


@teams_bp.route('/<int:team_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(team_id, user_id):
    team = Team.query.get_or_404(team_id)
    if current_user.role not in ('manager', 'admin') and current_user.id != team.lead_id:
        abort(403)

    user = db.session.get(User, user_id)
    if user and user in team.members.all():
        team.members.remove(user)
        db.session.commit()
        flash(f'{user.username} removed from team.', 'success')

    return redirect(url_for('teams.detail', team_id=team.id))


@teams_bp.route('/<int:team_id>/join', methods=['POST'])
@login_required
def join(team_id):
    team = Team.query.get_or_404(team_id)
    if current_user not in team.members.all():
        team.members.append(current_user)
        db.session.commit()
        flash(f'You joined "{team.name}".', 'success')
    return redirect(url_for('teams.detail', team_id=team.id))


@teams_bp.route('/<int:team_id>/leave', methods=['POST'])
@login_required
def leave(team_id):
    team = Team.query.get_or_404(team_id)
    if current_user in team.members.all():
        team.members.remove(current_user)
        db.session.commit()
        flash(f'You left "{team.name}".', 'success')
    return redirect(url_for('teams.detail', team_id=team.id))
