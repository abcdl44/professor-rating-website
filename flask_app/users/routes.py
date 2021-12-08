from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdatePasswordForm, UpdateEmailForm
from ..models import User, Review
from .. import bcrypt

users = Blueprint('users', __name__)

# account, create account, login, user page, logout

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()
    password_form = UpdatePasswordForm()
    email_form = UpdateEmailForm()

    if username_form.submit.data and username_form.validate():
        user = User.objects(username=current_user.get_id()).first()
        user.modify(username=username_form.username.data)
        logout_user()
        login_user(user)
        return redirect(url_for('users.account'))
    if password_form.submit.data and password_form.validate():
        user = User.objects(username=current_user.get_id()).first()
        hashed = bcrypt.generate_password_hash(password_form.password.data).decode("utf-8")
        user.modify(password=hashed)
        logout_user()
        login_user(user)
        return redirect(url_for('users.account'))
    if email_form.submit.data and email_form.validate():
        user = User.objects(username=current_user.get_id()).first()
        user.modify(email=email_form.email.data)
        logout_user()
        login_user(user)
        return redirect(url_for('users.account'))
    reviews = Review.objects(commenter=current_user._get_current_object())
    return render_template("account.html", username_form = username_form, password_form=password_form, email_form=email_form, reviews=reviews)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("not_users.index"))

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        redirect(url_for("users.account"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("users.account"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
        else:
            flash("Invalid login credentials.")
            return redirect(url_for('users.login'))

    return render_template("login.html", form=form)

@users.route("/user/<username>", methods=["GET", "POST"])
def user_details(username):
    username = User.objects(username=username).first()
    reviews = Review.objects(commenter=username)
    return render_template("user_details.html", user=username, reviews = reviews)