from datetime import datetime
from models import db


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    color = db.Column(db.String(7), default='#2563eb')  # hex color for badge
    lead_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lead = db.relationship('User', foreign_keys=[lead_id], backref='led_teams')
    tasks = db.relationship('Task', backref='team', lazy='dynamic')

    @property
    def member_count(self):
        return self.members.count()

    @property
    def open_tasks_count(self):
        return self.tasks.filter(Task.status != 'done').count()

    def __repr__(self):
        return f'<Team {self.name}>'


# Avoid circular import
from models.task import Task
