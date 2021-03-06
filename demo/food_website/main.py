from . import db
from .models import User, FoodItem, FoodData
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from datetime import date
from datetime import datetime
import calendar
import requests
import json
import pytz
import math

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    foods = user.foods

    my_date = datetime.now(pytz.timezone('US/Pacific'))
    bar_labels = []
    bar_values = []
    count = 0
    maxVal = 0
    for i in range(30):
        totalCalorie = 0
        for food in foods:
            my_datetime = subtract_date(my_date, i)
            if my_datetime.date() == food.date_posted.date():
                totalCalorie = totalCalorie + food.calorie
        my_datetime = subtract_date(my_date, i).strftime('%#m/%#d')
        bar_labels.append(my_datetime)
        bar_values.append(totalCalorie)
        if totalCalorie > maxVal:
            maxVal = totalCalorie

    maxVal = int(math.ceil(maxVal / 100.0)) * 100

    return render_template('profile.html', name=current_user.name, title='Calorie History', max=maxVal, labels=bar_labels, values=bar_values)


def subtract_date(my_date, i):
    if my_date.day + (i-29) <= 0:
        daysInMonth = calendar.monthrange(my_date.year, my_date.month - 1)[1]
        return datetime(my_date.year, my_date.month - 1, my_date.day + (i + daysInMonth - 29))
    else:
        return datetime(my_date.year, my_date.month, my_date.day + (i-29))


@main.route("/all")
@login_required
def user_fooditems():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    foods = user.foods
    totalCalorie = 0

    #my_date = date.today()
    my_date = datetime.now(pytz.timezone('US/Pacific'))
    my_datetime = datetime(my_date.year, my_date.month, my_date.day)

    foods.sort()
    foods.reverse()

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
    return redirect(url_for('main.user_fooditems'))


@main.route("/fooditem/add/<int:cal>/<string:food>", methods=['GET', 'POST'])
@login_required
def add_search(food, cal):
    food_name = food
    calorie = cal

    my_date = datetime.now(pytz.timezone('US/Pacific'))
    date_post = str(datetime(my_date.year, my_date.month, my_date.day))
    date = datetime.strptime(date_post, '%Y-%m-%d %H:%M:%S')

    print(calorie, date, food_name)
    food = FoodItem(food_name=food_name, date_posted=date,
                    calorie=calorie, author=current_user)
    db.session.add(food)
    db.session.commit()
    flash('Your food item has been added!')
    return redirect(url_for('main.user_fooditems'))


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
        nutrition_info = (result_string[0][6],result_string[0][9],result_string[0][3]), (result_string[1][6],result_string[1][9],result_string[1][3]), (result_string[2][6],result_string[2][9],result_string[2][3])
        return render_template('result.html', item_name=item_name, item_calorie=item_calorie, nutrition_info=nutrition_info)
    except:
        return render_template('result_fail.html')


def food_api_request(food):
    site = "https://api.nutritionix.com/v1_1/search/{}?results=0:20&fields=item_name,brand_name,item_id,nf_calories,nf_saturated_fat,nf_total_fat,nf_cholesterol,nf_sodium,nf_total_carbohydrate,nf_dietary_fiber,nf_sugars,nf_protein&appId=e3a7c4fc&appKey=4f44386d9119e50a1cc5fac766e51197".format(
        food)
    response = requests.get(site)
    jsontext = json.loads(response.text)
    foodnames = []
    for i in range(3):
        pair = (jsontext["hits"][i]["fields"]["item_name"],
                jsontext["hits"][i]["fields"]["nf_calories"],
                jsontext["hits"][i]["fields"]["nf_saturated_fat"],
                jsontext["hits"][i]["fields"]["nf_total_fat"],
                jsontext["hits"][i]["fields"]["nf_cholesterol"],
                jsontext["hits"][i]["fields"]["nf_sodium"],
                jsontext["hits"][i]["fields"]["nf_total_carbohydrate"],
                jsontext["hits"][i]["fields"]["nf_dietary_fiber"],
                jsontext["hits"][i]["fields"]["nf_sugars"],
                jsontext["hits"][i]["fields"]["nf_protein"])
        foodnames.append(pair)
    return foodnames
