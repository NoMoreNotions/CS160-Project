from . import db
from .models import User
from .models import FoodItem
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route("/all")
@login_required
def user_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    # Workout.query.filter_by(author=user).order_by(Workout.date_posted.desc())
    foods = user.foods
    totalCalorie = 0
    for food in foods:
        totalCalorie = totalCalorie + food.calorie
    return render_template('all_workouts.html', foods=foods, user=user, totalCalorie=totalCalorie)


@main.route("/new")
@login_required
def new_workout():
    return render_template('create_workout.html')


@main.route("/new", methods=['POST'])
@login_required
def new_workout_post():
    food_name = request.form.get('food-name')
    calorie = request.form.get('calorie')

    print(calorie, food_name)
    food = FoodItem(food_name=food_name,
                    calorie=calorie, author=current_user)
    db.session.add(food)
    db.session.commit()
    flash('Your food item has been added!')
    return redirect(url_for('main.index'))


@main.route("/workout/<int:food_id>/update", methods=['GET', 'POST'])
@login_required
def update_workout(food_id):
    food = FoodItem.query.get_or_404(food_id)
    if request.method == "POST":
        food.food_name = request.form['food-name']
        food.calorie = request.form['calorie']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.user_workouts'))

    return render_template('update_workout.html', food=food)


@main.route("/workout/<int:food_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_workout(food_id):
    food = FoodItem.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('main.user_workouts'))
