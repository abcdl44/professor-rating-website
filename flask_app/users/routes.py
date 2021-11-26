from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User

users = Blueprint('users', __name__)

# account, create account, login, user page, logout

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html")

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("not_users.index"))

@users.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@users.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@users.route("/user/<username>", methods=["GET", "POST"])
def user_details(username):
    return render_template("user_details.html")