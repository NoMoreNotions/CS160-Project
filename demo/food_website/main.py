from . import db
from .models import User, FoodItem, FoodData
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
import requests
import json

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
def user_fooditems():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    foods = user.foods
    totalCalorie = 0
    for food in foods:
        totalCalorie = totalCalorie + food.calorie
    return render_template('all_fooditems.html', foods=foods, user=user, totalCalorie=totalCalorie)


@main.route("/new")
@login_required
def new_fooditem():
    return render_template('create_fooditem.html')


@main.route("/new", methods=['POST'])
@login_required
def new_fooditem_post():
    food_name = request.form.get('food-name')
    calorie = request.form.get('calorie')

    print(calorie, food_name)
    food = FoodItem(food_name=food_name,
                    calorie=calorie, author=current_user)
    db.session.add(food)
    db.session.commit()
    flash('Your food item has been added!')
    return redirect(url_for('main.index'))


@main.route("/fooditem/<int:food_id>/update", methods=['GET', 'POST'])
@login_required
def update_fooditem(food_id):
    food = FoodItem.query.get_or_404(food_id)
    if request.method == "POST":
        food.food_name = request.form['food-name']
        food.calorie = request.form['calorie']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.user_fooditems'))

    return render_template('update_fooditem.html', food=food)


@main.route("/fooditem/<int:food_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_fooditem(food_id):
    food = FoodItem.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('main.user_fooditems'))


@main.route("/search")
@login_required
def search():
    return render_template('search.html')


@main.route("/search", methods=['POST'])
@login_required
def search_post():
    food_name = request.form.get('food-name')
    result_string = food_api_request(food_name)
    print(result_string)
    item_name = result_string[0][0], result_string[1][0], result_string[2][0]
    item_calorie = result_string[0][1], result_string[1][1], result_string[2][1]
    return render_template('result.html', item_name=item_name, item_calorie=item_calorie)


def food_api_request(food):
    site = "https://api.nutritionix.com/v1_1/search/{}?results=0:20&fields=item_name,brand_name,item_id,nf_calories&appId=e3a7c4fc&appKey=4f44386d9119e50a1cc5fac766e51197".format(
        food)
    response = requests.get(site)
    jsontext = json.loads(response.text)
    foodnames = []
    for i in range(3):
        pair = (jsontext["hits"][i]["fields"]["item_name"],
                jsontext["hits"][i]["fields"]["nf_calories"])
        foodnames.append(pair)
    return foodnames
