import mysql.connector

db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root",
	database="testdb"
	)

mycursor = db.cursor()

#mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("DESCRIBE Person")

#mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Tim", 19))
#db.commit()

#mycursor.execute("CREATE TABLE User (name VARCHAR(50), pass VARCHAR(50))")
#mycursor.execute("DESCRIBE User")
#mycursor.execute("INSERT INTO User (name, pass) VALUES (%s,%s)", ("tim123", "pass1"))
#mycursor.execute("INSERT INTO User (name, pass) VALUES (%s,%s)", ("coolbob", "pass2"))
#mycursor.execute("INSERT INTO User (name, pass) VALUES (%s,%s)", ("alantheman", "pass3"))
#mycursor.execute("INSERT INTO User (name, pass) VALUES (%s,%s)", ("casey9", "pass4"))

#db.commit()


mycursor.execute("SELECT * FROM User")
for x in mycursor:
	print(x)

name = input("Username: ")

