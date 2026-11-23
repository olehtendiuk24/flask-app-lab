from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile("../config.py")
csrf = CSRFProtect(app)

from app import views
from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)