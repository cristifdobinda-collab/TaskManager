import threading
from flask import Blueprint, jsonify, current_app
from flask_login import login_required, current_user
from models import db
from models.notification import Notification
from models.user import User

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')


def notify_user(user_id, notif_type, message, link=None):
    """Create in-app notification and optionally send email."""
    user = db.session.get(User, user_id)
    if not user:
        return

    # Check user preferences
    pref_map = {
        'assignment': 'notify_assignment',
        'comment': 'notify_comments',
        'deadline': 'notify_deadlines',
        'overdue': 'notify_deadlines',
    }
    pref_attr = pref_map.get(notif_type)
    if pref_attr and not getattr(user, pref_attr, True):
        return

    notif = Notification(user_id=user_id, type=notif_type, message=message, link=link)
    db.session.add(notif)
    db.session.commit()

    # Send email async
    _send_email_async(user.email, message, link)


def _send_email_async(to_email, message, link):
    try:
        from flask import current_app
        app = current_app._get_current_object()

        def send():
            with app.app_context():
                try:
                    from flask_mail import Message
                    from app import mail
                    msg = Message('Task Manager Notification', recipients=[to_email])
                    msg.body = f'{message}\n\n{link or ""}'
                    mail.send(msg)
                except Exception:
                    pass  # Don't crash on email failure

        thread = threading.Thread(target=send)
        thread.start()
    except Exception:
        pass


@notifications_bp.route('/unread')
@login_required
def unread():
    notifications = Notification.query.filter_by(
        user_id=current_user.id, read=False
    ).order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify({
        'count': len(notifications),
        'notifications': [n.to_dict() for n in notifications],
    })


@notifications_bp.route('/<int:notif_id>/read', methods=['POST'])
@login_required
def mark_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id != current_user.id:
        return jsonify({'success': False}), 403
    notif.read = True
    db.session.commit()
    return jsonify({'success': True})


@notifications_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, read=False).update({'read': True})
    db.session.commit()
    return jsonify({'success': True})
