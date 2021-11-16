from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class AppUsers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(150))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    goalWeight = db.Column(db.Integer)


class CalorieInfo(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(200), nullable=False)
    calorie = db.Column(db.Integer, nullable=False)
