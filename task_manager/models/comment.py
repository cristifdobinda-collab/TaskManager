from datetime import datetime
from models import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'
