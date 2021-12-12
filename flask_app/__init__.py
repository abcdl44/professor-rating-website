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
from flask_mail import Mail

from datetime import datetime
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

from .not_users.routes import not_users
from .users.routes import users

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
    app.config["SECRET_KEY"] = os.urandom(16)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ProfessorRater2021@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Password2021'
    app.config['MAIL_DEFAULT_SENDER'] = 'ProfessorRater2021@gmail.com'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    if test_config is not None:
        app.config.update(test_config)
 
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_blueprint(users)
    app.register_blueprint(not_users)

    login_manager.login_view = "users.login"

    return app