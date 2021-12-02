import datetime
from datetime import datetime, timedelta
import hashlib
import random
from random import randint


foods = {
	"Ramen Noodles - 1 cup":		157,
	"Beef Pho - 1 bowl":		637,
	"Caesar Salad":	160,
	"Curry Rice":	224,
	'Chicken Burrito - 1 large burrito':       930, 
	'Soft Beef Taco':       230,
	'Mac and Cheese':      220,
	'Pad Thai':        560,
	'Beef Chow Fun - 1 serving':	867,
	'Banh Mi - 1 sandwich':  600,
	'Tuna Salad Sandwich':       438,
	'Orange Juice - 1 cup':       111,
	'Apple':       125,
	'Banana':       105,
	'Potato chips, plain, salted - 1 bag':       297,
	'Strawberry Banana Smoothie - 1 cup':       161,
	'Cheese Pizza - 1 small slice':       149,
	'Cheeseburger': 	500,
	'Hawaiian Pizza - 1 large slice':		348,
	'Chicken Noodle Soup':		120,
	'Grilled Cheese - 1 sandwich':		365,
	'Sprite - 1 medium cup 21 fl oz':		194
}
foodIDs = {}

#main = "USE caloriedb;\nDROP TABLE appusers;\nDROP TABLE calorieinfo;\nDROP TABLE foodhistory;\n\nCREATE TABLE AppUsers\n(userID int PRIMARY KEY AUTO_INCREMENT,\nusername VARCHAR(255) NOT NULL,\npassword VARCHAR(255) NOT NULL,\nage smallint,\nweight int,\nheight int,\ngoalWeight int\n);\n\nCREATE TABLE CalorieInfo\n(itemID int PRIMARY KEY,\nfoodName VARCHAR(255) NOT NULL,\ncalorie int NOT NULL\n);\n\nCREATE TABLE FoodHistory\n(itemID int,\nuserID int,\nquantity int NOT NULL,\ndateInfo date\n);\n\n"
main = ""

# CHANGE PARAMETERS HERE #
userCount = 8
ageRange = (20, 40)
weightRange = (150, 250)
heightRange = (150, 200)
goalRange = (-40, -10)
quantityRange = (1, 2)
calorieRange = (1700, 2200)
dateRange = 30
fidStart = 9

###
def parse(a, b):
	global main
	if a < b:
		main += ",\n"
	else:
		main += ";\n\n"

main += "INSERT INTO food_item VALUES\n"

for d in range(dateRange + 1):
	dateValue = datetime.today() - timedelta(days=(d))
	calorieRange = (1700 + d*5, 2200 + d*5)
	calRandom = randint(calorieRange[0], calorieRange[1])
	calCount = 0
	while calCount < calRandom:
		#quantity = randint(quantityRange[0], quantityRange[1])
		food, cal = random.choice(list(foods.items()))
		calCount += cal
		userID = 1
		main += "({}, '{}', '{}', {}, {})".format(fidStart, food, dateValue, cal, userID)
		main += ",\n"
		fidStart += 1

	if d % 7 == 0 and d != 0 and d != dateRange:
		main = main[0:-2]
		main += ";\n\nINSERT INTO food_item VALUES\n"

main = main[0:-2]
main += ";"

#print(main)

with open("sample_database.sql", "w") as text_file:
    text_file.write(main)