from . import db
from .models import User, FoodItem, FoodData
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from datetime import date
from datetime import datetime
import requests
import json
import pytz
#import pandas as pd
#import matplotlib.pyplot as plt

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    foods = user.foods

    #hist = {}

    #for i in range(7):
        #totalCalorie = 0

        #my_date = date.today()
        #my_datetime = datetime(my_date.year, my_date.month, my_date.day-i)

        #for food in foods:
            #if my_datetime.date() == food.date_posted.date():
                #totalCalorie = totalCalorie + food.calorie

        #hist[my_datetime] = totalCalorie

        #s = pd.Series({"calories": hist})
        #fig, ax = plt.subplots()
        #s.plot.bar(list(hist.keys()), hist.values(), color='g')
        #fig.savefig('my_plot.png')

    return render_template('profile.html', name=current_user.name)


@main.route("/all")
@login_required
def user_fooditems():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    foods = user.foods
    totalCalorie = 0

    #my_date = date.today()
    my_date = datetime.now(pytz.timezone('US/Pacific'))
    my_datetime = datetime(my_date.year, my_date.month, my_date.day)

    for food in foods:
        if my_datetime.date() == food.date_posted.date():
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
    date_post = request.form.get('food-date')
    calorie = request.form.get('calorie')

    date = datetime.strptime(date_post, "%Y-%m-%d")

    print(calorie, date, food_name)
    food = FoodItem(food_name=food_name, date_posted=date,
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
    try:
        result_string = food_api_request(food_name)
        print(result_string)
        item_name = result_string[0][0], result_string[1][0], result_string[2][0]
        item_calorie = result_string[0][1], result_string[1][1], result_string[2][1]
        return render_template('result.html', item_name=item_name, item_calorie=item_calorie)
    except:
        return render_template('result_fail.html')


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
