import hashlib
from datetime import datetime
from flask_login import UserMixin
import bcrypt
from models import db

team_members = db.Table(
    'team_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('role', db.String(20), default='member'),  # member, lead
    db.Column('joined_at', db.DateTime, default=datetime.utcnow),
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120), default='')
    job_title = db.Column(db.String(120), default='')
    department = db.Column(db.String(120), default='')
    bio = db.Column(db.Text, default='')
    role = db.Column(db.String(20), default='user')  # user, manager, admin
    is_active = db.Column(db.Boolean, default=True)
    notify_assignment = db.Column(db.Boolean, default=True)
    notify_comments = db.Column(db.Boolean, default=True)
    notify_deadlines = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    tasks_created = db.relationship('Task', foreign_keys='Task.creator_id', backref='creator', lazy='dynamic')
    tasks_assigned = db.relationship('Task', foreign_keys='Task.assignee_id', backref='assignee', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    teams = db.relationship('Team', secondary=team_members, backref=db.backref('members', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def gravatar(self, size=80):
        digest = hashlib.md5(self.email.lower().strip().encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @property
    def display_name(self):
        return self.full_name or self.username

    @property
    def tasks_completed_count(self):
        return self.tasks_assigned.filter_by(status='done').count()

    @property
    def tasks_active_count(self):
        return self.tasks_assigned.filter(
            db.not_(db.Column('status').in_(['done']))
        ).count()

    def __repr__(self):
        return f'<User {self.username}>'
