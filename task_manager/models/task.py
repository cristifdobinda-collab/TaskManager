from datetime import datetime
from models import db

task_tags = db.Table(
    'task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, review, done
    deadline = db.Column(db.DateTime, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('Tag', secondary=task_tags, backref=db.backref('tasks', lazy='dynamic'))
    comments = db.relationship('Comment', backref='task', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def is_overdue(self):
        if self.deadline and self.status != 'done':
            return datetime.utcnow() > self.deadline
        return False

    @property
    def priority_class(self):
        return {'low': 'success', 'medium': 'info', 'high': 'warning', 'critical': 'error'}.get(self.priority, 'info')

    @property
    def status_label(self):
        return {'todo': 'To Do', 'in_progress': 'In Progress', 'review': 'Review', 'done': 'Done'}.get(self.status, self.status)

    def __repr__(self):
        return f'<Task {self.title}>'
