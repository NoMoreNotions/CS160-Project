import mysql.connector
import datetime as date
from datetime import datetime, timedelta
import hashlib

# NOTES:
# - replace print statements with POST/GET requests for HTML integration
# - make stronger password checks for user creation
# - use test_case_generator.py to create a sample database
# - run main.py in python terminal to test functions on sample database

# CHANGE USER/PASS TO WORK WITH MYSQL WORKBENCH #
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root",
	database="caloriedb"
	)

mycursor = db.cursor()

userID = ''
loggedIn = False

# crosscheck database with login credentials
def login(user, passwd):
	global loggedIn, userID
	mycursor.execute("SELECT * FROM AppUsers WHERE username=\"{}\"".format(user))
	if mycursor.fetchone() != None:
		mycursor.execute("SELECT password FROM AppUsers WHERE username='{}'".format(user))
		if mycursor.fetchone()[0] == hashlib.sha256(passwd.encode()).hexdigest():
			print("Log in successful.")
			mycursor.execute("SELECT userID FROM AppUsers WHERE username='{}'".format(user))
			userID = mycursor.fetchone()[0]
			loggedIn = True
		else:
			print("Incorrect password.")
	else:
		print("User does not exist.")

# adds food to database given food name with quantity and date of consumption, only if user is logged in
def addFoodDate(food, quantity, dateValue):
	if loggedIn == True:
		mycursor.execute("SELECT itemID FROM CalorieInfo WHERE foodName='{}'".format(food))
		results = mycursor.fetchone()
		if results != None:
			foodID = results[0]
			time = dateValue
			mycursor.execute("INSERT INTO FoodHistory (itemID, userID, quantity, dateInfo) VALUES ({}, {}, {}, '{}')".format(foodID, userID, quantity, time))
			db.commit()
			print("Food added successfully.")
		else:
			print("Food does not exist in the database.")
	else:
		print("Please sign in.")

# adds food to database with date of consumption set to current time
def addFood(food, quantity):
	addFoodDate(food, quantity, date.datetime.now().strftime("%Y-%m-%d %H:%M"))

# view list of foods consumed on specified date
def viewFood(dateValue):
	if loggedIn == True:
		mycursor.execute("SELECT * FROM FoodHistory WHERE userID={} AND DATE_FORMAT(dateInfo, '%Y-%m-%d') = DATE_FORMAT('{}', '%Y-%m-%d')".format(userID, dateValue))
		idArr = []
		calArr = []
		foods = []
		for food in mycursor:
			idArr.append((food[0], food[2]))
		for i in range(len(idArr)):
			mycursor.execute("SELECT * FROM CalorieInfo WHERE itemID={}".format(idArr[i][0]))
			calArr.append(mycursor.fetchone())
			foods.append((idArr[i][1], calArr[i][1], calArr[i][2]))
		print(foods)
	else:
		print("Please sign in.")

# view number of calories consumed on specified date
def viewDayCal(dateValue, histBool):
	if loggedIn == True:
		mycursor.execute("SELECT * FROM FoodHistory WHERE userID={} AND DATE_FORMAT(dateInfo, '%Y-%m-%d') = DATE_FORMAT('{}', '%Y-%m-%d')".format(userID, dateValue))
		idArr = []
		calArr = []
		cals = []
		for food in mycursor:
			idArr.append((food[0], food[2]))
		for i in range(len(idArr)):
			mycursor.execute("SELECT * FROM CalorieInfo WHERE itemID={}".format(idArr[i][0]))
			calArr.append(mycursor.fetchone())
			cals.append(idArr[i][1] * calArr[i][2])
		if histBool == False:
			print("You consumed {} calories on {}.".format(sum(cals), dateValue))
		return cals
	else:
		print("Please sign in.")
		return None

# view past 30 day history of calories after specified date
def viewHistory(dateValue):
	sumArr = []
	for i in range(30):
		dv = datetime.strptime(dateValue, '%Y-%m-%d') + timedelta(days=i)
		calSum = viewDayCal(dv, True)
		if calSum == None:
			return None
		sumArr.append(sum(calSum))
	print(sumArr)

# show user details 
def showProfile():
	if loggedIn == True:
		mycursor.execute("SELECT * FROM AppUsers WHERE userID={}".format(userID))
		info = mycursor.fetchone()
		profile = "Username: {}\nAge: {}\nHeight: {} cm\nWeight: {} lbs\nWeight Goal: {} lbs\n".format(info[1], info[3], info[5], info[4], info[6])
		print(profile)
	else:
		print("Please sign in.")

# add user credentials to AppUsers table
def signUp(user, passwd):
	mycursor.execute("INSERT INTO AppUsers (username, password) VALUES ('{}', '{}')".format(user, hashlib.sha256(passwd.encode()).hexdigest()))
	print("Sign up successful. Please sign in.")

def logout():
	global loggedIn, userID
	userID = ''
	loggedIn = False
	print("Logout successful.")

# main terminal input loop
while True:	
	try:
		string = input("Input: ")
		inputArr = string.split(",")
		if inputArr[0] == "signup":
			signUp(inputArr[1], inputArr[2])
		elif inputArr[0] == "login":
			login(inputArr[1], inputArr[2])
		elif inputArr[0] == "logout":
			logout()
		elif inputArr[0] == "add":
			if len(inputArr) == 3:
				addFood(inputArr[1], int(inputArr[2]))
			elif len(inputArr) == 4:
				addFoodDate(inputArr[1], int(inputArr[2]), inputArr[3])
		elif inputArr[0] == "view":
			viewFood(inputArr[1])
		elif inputArr[0] == "profile":
			showProfile()
		elif inputArr[0] == "check":
			viewDayCal(inputArr[1], False)
		elif inputArr[0] == "history":
			viewHistory(inputArr[1])
		elif string == "exit":
			break
		else:
			print("Invalid command.")
	except:
		print("Invalid entry.")
	