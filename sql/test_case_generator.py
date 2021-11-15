import datetime
from datetime import datetime, timedelta
import hashlib
from multipledispatch import dispatch
import random
from random import randint

names = ["Adams","Baker","Clark","Davis","Evans","Frank","Ghosh","Hills","Irwin","Jones","Klein","Lopez","Mason","Nalty","Ochoa","Patel","Quinn","Reily","Smith","Trott","Usman","Valdo","White","Xiang","Yakub","Zafar"]
foods = {
	"Apples":		100,
	"Pretzels":		300,
	"Ham Sandwich":	300,
	"Apple Pie":	500,
	'Burger':       540, 
	'Apples':       20,
	'Bananas':      20,
	'Pasta':        320,
	'Mocha Latte':  60,
	'Coffee':       0,
	'Kitkat':       210
}
foodIDs = {}

main = "USE caloriedb;\nDROP TABLE appusers;\nDROP TABLE calorieinfo;\nDROP TABLE foodhistory;\n\nCREATE TABLE AppUsers\n(userID int PRIMARY KEY AUTO_INCREMENT,\nusername VARCHAR(255) NOT NULL,\npassword VARCHAR(255) NOT NULL,\nage smallint,\nweight int,\nheight int,\ngoalWeight int\n);\n\nCREATE TABLE CalorieInfo\n(itemID int PRIMARY KEY,\nfoodName VARCHAR(255) NOT NULL,\ncalorie int NOT NULL\n);\n\nCREATE TABLE FoodHistory\n(itemID int,\nuserID int,\nquantity int NOT NULL,\ndateInfo date\n);\n\n"

# CHANGE PARAMETERS HERE #
userCount = 10
ageRange = (20, 30)
weightRange = (150, 250)
heightRange = (150, 200)
goalRange = (-40, -10)
quantityRange = (1, 2)
calorieRange = (1500, 2500)
dateRange = 15
fidStart = 100

###
def parse(a, b):
	global main
	if a < b:
		main += ",\n"
	else:
		main += ";\n\n"

main += "INSERT INTO AppUsers VALUES\n" 

for i in range(userCount):
	weight = randint(weightRange[0],weightRange[1])
	main += "({}, '{}', '{}', {}, {}, {}, {})".format(i+1, random.choice(names)+str(i+1), hashlib.sha256(("pass"+str(i+1)).encode()).hexdigest(), randint(ageRange[0],ageRange[1]), weight, randint(heightRange[0],heightRange[1]), weight + randint(goalRange[0],goalRange[1]))
	parse(i, userCount - 1)

main += "INSERT INTO CalorieInfo VALUES\n"

count = 0
for x,y in foods.items():
	main += "({}, '{}', {})".format(fidStart + count, x, y)
	foodIDs[x] = fidStart + count 
	count += 1
	parse(count, len(foods))

#print(main)

main += "INSERT INTO FoodHistory VALUES\n"

for d in range(dateRange + 1):
	dateValue = datetime.today() - timedelta(days=(dateRange-d))
	for u in range(userCount):
		calRandom = randint(calorieRange[0], calorieRange[1])
		calCount = 0
		while calCount < calRandom:
			quantity = randint(quantityRange[0], quantityRange[1])
			food, cal = random.choice(list(foods.items()))
			calCount += quantity * cal
			main += "({}, {}, {}, '{}')".format(foodIDs.get(food), u+1, quantity, dateValue)
			main += ",\n"

main = main[0:-2]
main += ";"

#print(main)

with open("calorie.sql", "w") as text_file:
    text_file.write(main)