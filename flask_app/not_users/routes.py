# index, professor's pages, add new professor page

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from ..forms import AddNewProfessorForm, SearchForm, SubmitReviewForm
from ..models import Review, User, Professor
from ..utils import current_time
from .. import db

not_users = Blueprint('not_users', __name__)

@not_users.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("not_users.search_results", search=form.search_query.data))

    return render_template("index.html", form=form)

@not_users.route("/search_results/<search>", methods=["GET"])
def search_results(search):
    results = Professor.objects(name__contains=search)
    return render_template("search_results.html", results = results)


@not_users.route("/professor/<professor>", methods=["GET", "POST"])
def professor_page(professor):
    form = SubmitReviewForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        new_review = Review(
            commenter = current_user._get_current_object(),
            professor = professor,
            date = current_time(),
            rating = form.rating.data,
            text = form.text.data
        )
        new_review.save()

        # idk if this actually works
        Professor.objects(name = professor).update_one(inc__total_score=form.rating.data, inc__num_reviewers=1)
        # prof.save()

        return redirect(url_for("not_users.professor_page", professor=professor))

    reviews = Review.objects(professor=professor)
    professor_object = Professor.objects(name=professor).first()

    return render_template("professor_page.html", professor=professor_object, reviews = reviews, form = form)

@not_users.route("/add_new_professor", methods=["GET", "POST"])
@login_required
def add_new_professor():
    form = AddNewProfessorForm()
    if form.validate_on_submit():
        new_professor = Professor(
            name = form.name.data,
            total_score = 0,
            num_reviewers = 0
        )
        new_professor.save()
        return redirect(url_for("not_users.index"))
        # (professor_page(form.name.data))

    return render_template("add_new_professor.html", form = form)