from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
email = Mail()

login = LoginManager()
login.login_view = 'auth.login'

sess = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    sess.init_app(app)
    email.init_app(app)

    # avoiding circular dependencies
    from app.auth import bp as auth_bp
    from app.errors import bp as errors_bp
    from app.users import bp as users_bp
    from app.posts import bp as posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(errors_bp)

    return app


from app import models
