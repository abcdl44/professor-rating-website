# index, professor's pages, add new professor page

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from matplotlib import pyplot as plt
import io
import base64

from ..forms import AddNewProfessorForm, SearchForm, SubmitReviewForm
from ..models import Review, Professor
from ..utils import current_time
from .. import db

not_users = Blueprint('not_users', __name__)

@not_users.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    data = Professor.objects[:5]
    names = []
    ratings = []
    print(data)
    for i in data:
        names.append(i.name)
        count = 0
        sum = 0
        reviews = Review.objects(professor=i.name)
        for j in reviews:
            count += 1
            sum += j.rating
        if count == 0:
            ratings.append(0)
        else:
            ratings.append(sum//count)
    ax = plt.gca()
    ax.set_ylim([0, 10])
    plt.bar(names, ratings, color='xkcd:sky blue')
    plt.ylabel("Ratings")
    plt.title("Most rated professors")
    
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    img = base64.b64encode(my_stringIObytes.getvalue()).decode('utf-8')

    if form.validate_on_submit():
        return redirect(url_for("not_users.search_results", search=form.search_query.data))

    return render_template("index.html", form=form, img=img)

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
            text = form.text.data,
        )
        new_review.save()

        return redirect(request.path)

    reviews = Review.objects(professor=professor)
    
    professor_object = Professor.objects(name=professor).first()

    count = 0
    sum = 0
    reviews = Review.objects(professor=professor)
    for j in reviews:
        count += 1
        sum += j.rating
    overall = 0
    if count != 0:
        overall = sum//count

    return render_template("professor_page.html", professor=professor_object, reviews = reviews, form = form, score = overall)

@not_users.route("/add_new_professor", methods=["GET", "POST"])
@login_required
def add_new_professor():
    form = AddNewProfessorForm()
    if form.validate_on_submit():
        new_professor = Professor(
            name = form.name.data,
        )
        new_professor.save()
        return redirect(url_for("not_users.professor_page", professor=form.name.data))
        # (professor_page(form.name.data))

    return render_template("add_new_professor.html", form = form)

@not_users.route("/about", methods=["GET"])
def about():
    return render_template("about.html")