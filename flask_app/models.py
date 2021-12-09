from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return self.username

class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    professor = db.StringField(required=True, unique=True)
    date = db.StringField(required=True)
    rating = db.IntField(required=True)
    text = db.StringField(max_length=500)

class Professor(db.Document):
    name = db.StringField(required=True, unique=True)
    total_score = db.IntField(required=True)
    num_reviewers = db.IntField(required=True)
