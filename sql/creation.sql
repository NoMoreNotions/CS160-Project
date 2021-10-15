CREATE TABLE users 
(user_ID int PRIMARY KEY AUTO_INCREMENT
name VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
age smallint UNSIGNED,
weight int,
height int,
goalWeight int
);

CREATE TABLE foodHistory
(
itemID int PRIMARY KEY AUTO_INCREMENT,
foreign key (user_ID) references users,
foodName VARCHAR(255) NOT NULL,
calorie int NOT NULL,
quantity int DEFAULT 1,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);

