from datetime import datetime
from models import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # assignment, comment, deadline, overdue
    message = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(200), nullable=True)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'message': self.message,
            'link': self.link,
            'read': self.read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
        }

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'
