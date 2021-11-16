from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class AppUsers(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(150))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    hieght = db.Column(db.Integer)
    goalWeight = db.Column(db.Integer)


class CalorieInfo(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(200), nullable=False)
    calorie = db.Column(db.Integer, nullable=False)


class FoodHistory(db.Model):
    itemId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    dateInfo = db.Column(db.date)
