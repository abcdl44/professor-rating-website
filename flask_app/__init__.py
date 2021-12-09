from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from datetime import datetime
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

from .not_users.routes import not_users
from .users.routes import users

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_blueprint(users)
    app.register_blueprint(not_users)

    login_manager.login_view = "users.login"

    return app