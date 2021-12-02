from flask_login import UserMixin
from datetime import datetime
from . import db


class User(db.Model, UserMixin):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    foods = db.relationship('FoodItem', backref='author', lazy=True)


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    calorie = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __lt__(self, other):
        return self.date_posted < other.date_posted


class FoodData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Text, nullable=False)
    calorie = db.Column(db.Integer, nullable=False)
