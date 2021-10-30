CREATE TABLE AppUsers
(user_ID int PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
age smallint,
weight int,
height int,
goalWeight int
);

CREATE TABLE FoodHistory
(itemID int,
user_ID int,
foodName VARCHAR(255) NOT NULL,
calorie int NOT NULL,
quantity int NOT NULL,
PRIMARY KEY (user_ID, itemID),
FOREIGN KEY (user_ID) REFERENCES users (user_ID) ON DELETE CASCADE
);

