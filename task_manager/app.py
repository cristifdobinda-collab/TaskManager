import re
from datetime import datetime
from markupsafe import Markup, escape
from flask import Flask
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.dashboard import dashboard_bp
    from routes.profile import profile_bp
    from routes.admin import admin_bp
    from routes.notifications import notifications_bp
    from routes.teams import teams_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(teams_bp)

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            from models.notification import Notification
            count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
            return {'unread_count': count}
        return {'unread_count': 0}

    @app.template_filter('render_mentions')
    def render_mentions(text):
        """Replace @username with highlighted spans in comment text."""
        escaped = escape(text)
        def replace_mention(match):
            username = match.group(1)
            return Markup(f'<span class="mention">@{username}</span>')
        return Markup(re.sub(r'@([\w.\-]+)', replace_mention, str(escaped)))

    with app.app_context():
        # Import all models so tables are created
        from models.team import Team
        from models.task import Task
        from models.comment import Comment
        from models.notification import Notification
        db.create_all()

    return app
