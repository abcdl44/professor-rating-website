from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    ValidateLessThanOrEqual,
    ValidateGreaterThanOrEqual,
    Optional
)

from .models import User


# Search form
class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

# Account Creation Form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=30)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

# Username Update Form
class UpdateUsernameForm(FlaskForm):
    username = StringField("New Username", validators=[InputRequired(), Length(min=1, max=20)])
    submit = SubmitField("Update Username")

# Password Update Form
class UpdatePasswordForm(FlaskForm):
    password = StringField("New Password", validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField("Update Password")

# Email Update Form
class UpdateEmailForm(FlaskForm):
    email = StringField("New Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Update email")

# Submit Review about Professor
class SubmitReviewForm(FlaskForm):
    rating = IntegerField("Rating", validators=[InputRequired(), ValidateGreaterThanOrEqual(value=1), ValidateLessThanOrEqual(value=10)])
    text = TextAreaField("Comment", Length(max=500), Optional())
    submit = SubmitField("Add Review")

# Add new professor
# Does this need anything besides a name? I guess a school, if we're doing that
class AddNewProfessorForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Add Professor")

# Add new school (?), idk are we even doing this?
class AddNewSchool(FlaskForm):
    name = StringField("School Name", validators=[InputRequired()])
    submit = SubmitField("Add School")