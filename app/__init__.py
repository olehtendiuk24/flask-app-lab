import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from app.config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from app import views
        from app.users import users_bp
        from app.products import products_bp
        from app.posts import post_bp

        app.register_blueprint(users_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(post_bp)

    return app