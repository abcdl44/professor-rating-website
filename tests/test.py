import pytest

from types import SimpleNamespace

from flask_app.forms import (SearchForm, 
                            RegistrationForm, 
                            UpdateUsernameForm, 
                            UpdatePasswordForm, 
                            LoginForm,
                            AddNewProfessorForm,
                            SubmitReviewForm)
from flask_app.models import User, Review, Professor
from flask import session


# tests:
# load site as a whole
# register account, login
# change username, password
# add prof, search for that proj
# add review



def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200


@pytest.mark.parametrize(
    ("username", "password", "email"), 
    (
        ("abc", "abcd", "test@test.co"),
        ("sdaf", "blarg", "blah@nla.com"),
    )
)
def test_register(client, username, password, email):
    login = SimpleNamespace(username=username, password=password, email=email, confirm_password=password, submit="Create Account")
    registration = RegistrationForm(formdata=None, obj=login)

    client.post("/register", data=registration.data, follow_redirects=True)
    user = User.objects(username=username).first()
    assert user is not None

def test_login(client, auth):
    resp = client.get("/login")
    assert resp.status_code == 200

    auth.register()
    auth.login()
    with client:
        client.get("/")
        assert session["_user_id"] == "test"
    auth.logout()
    assert resp.status_code == 302
    resp = client.get('/account', follow_redirects=True)
    assert resp.status_code == 200
    assert b"login" in resp.data

def test_change_username(client, auth):
    auth.register()
    auth.login()
    resp = client.get('/account')
    assert resp.status_code == 200

    newUser = "test2"
    name = SimpleNamespace(username=newUser, submit="Update Username")
    form = UpdateUsernameForm(formdata=None, obj=name)
    resp=client.post("/account", data=form.data, follow_redirects=True)
    assert resp.status_code == 200

    auth.login("test2", "test")
    resp = client.get('/account')
    assert b'test2' in resp.data
    user = User.objects(username="test2").first()
    assert user is not None

def test_change_password(client, auth):
    auth.register()
    auth.login()

    newPW = "password2"
    pw = SimpleNamespace(password=newPW, submit="Update Password")
    form = UpdatePasswordForm(formdata=None, obj=pw)
    resp=client.post("/account", data=form.data, follow_redirects=True)
    assert resp.status_code == 200

    login = SimpleNamespace(username="test", password="password2", submit="Login")
    form = LoginForm(formdata=None, obj=login)
    resp = client.post("/login", data=form.data, follow_redirects=True)
    with client:
        client.get("/")
        assert session["_user_id"] == "test"

@pytest.mark.parametrize(
    ("name"), 
    (
        ("abc"),
        ("sdaf"),
    )
)
def test_add_prof(client, auth, name):
    auth.register()
    auth.login()

    prof = SimpleNamespace(name=name, submit="Add Professor")
    form = AddNewProfessorForm(formdata=None, obj=prof)
    resp=client.post("/add_new_professor", data=form.data, follow_redirects=True)
    prof = Professor.objects(name=name).first()
    assert resp.status_code == 200
    assert prof is not None
    assert b"professor" in resp.data

def test_add_review(client, auth):
    auth.register()
    auth.login()

    prof = SimpleNamespace(name="prof", submit="Add Professor")
    form = AddNewProfessorForm(formdata=None, obj=prof)
    client.post("/add_new_professor", data=form.data, follow_redirects=True)

    review=SimpleNamespace(rating=5, text="he bad.", submit="Add Professor")
    form = SubmitReviewForm(formdata=None, obj=review)
    resp = client.post("/professor/prof", data=form.data, follow_redirects=True)
    assert resp.status_code == 200

    rev = Review.objects(professor="prof").first()
    assert rev is not None
    assert b'bad' in resp.data

