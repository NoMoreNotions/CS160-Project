DROP TABLE AppUsers;
DROP TABLE FoodHistory;
DROP TABLE CalorieInfo;

CREATE TABLE AppUsers
(userID int PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
age smallint,
weight int,
height int,
goalWeight int
);

CREATE TABLE FoodHistory
(itemID int,
userID int,
quantity int NOT NULL,
dateInfo date,
PRIMARY KEY (userID, itemID),
FOREIGN KEY (userID) REFERENCES users (userID) ON DELETE CASCADE
);

CREATE TABLE CalorieInfo
(itemID int,
foodName VARCHAR(255) NOT NULL,
calorie int NOT NULL
);

INSERT INTO AppUsers VALUES 
(1, 'Martin',  'sfq213',       31, 180, 150, 200),
(2, 'Arya',    'sfaseq123',    18, 200, 165, 150),
(3, 'Jake',    'gsas12',       24, 109, 120, 160),
(4, 'Tran',    'Cassidy223',   22, 240, 190, 160);

INSERT INTO CalorieInfo VALUES 
(102, 'Burger',       540), 
(622, 'Apples',       20),
(272, 'Bananas',      20),
(978, 'Pasta',        320),
(323, 'Mocha Latte',  60),
(304, 'Coffee',       0),
(810, 'Kitkat',       210);

INSERT INTO FoodHistory VALUES 
(102, 1, 2, '2021-09-01 09:08'),
(622, 2, 2, '2021-10-02 00:00'),
(272, 2, 1, '2021-09-03 00:00'),
(978, 2, 1, '2021-08-04 00:00'),
(323, 3, 1, '2021-09-05 00:00'),
(304, 2, 1, '2021-10-06 00:00'),
(810, 4, 3, '2021-08-07 00:00');