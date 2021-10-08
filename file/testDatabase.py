import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "testDb"
)

cursor = db.cursor()
#cursor.execute("CREATE TABLE users (name VARCHAR(255),age smallint UNSIGNED, user_ID int PRIMARY KEY AUTO_INCREMENT)")
#cursor.execute("CREATE TABLE foodTable (name VARCHAR(255),calories int UNSIGNED, food_ID int PRIMARY KEY AUTO_INCREMENT)")

##query = "INSERT INTO users (name, age) VALUES (%s, %s)"
#query2 = "INSERT INTO foodTable (name, calories) VALUES (%s, %s)"

## storing values in a variable
#values = [
#  ("Pepsi", 120),
 # ("Pizza (1 Slice)", 160),
 # ("Bread (1 Slice)", 75),
#  ("Fried Chicken Burger", 270)
#]

## executing the query with values
#cursor.executemany(query2, values)

userTableDisplay = "SELECT * FROM users"
foodTableDisplay = "Select * FROM foodTable"
cursor.execute(userTableDisplay)
print("User Database")
for user in cursor:
    print(user)

print("------------------------------")
print("Food Database")
cursor.execute(foodTableDisplay)
for food in cursor:
    print(food)


## to make final output we have to run the 'commit()' method of the database object
##db.commit()





