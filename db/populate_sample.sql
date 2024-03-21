-- Database: global_cafe

-- Populate User_Groups table
INSERT INTO User_Groups (group_id, discount_points, number_members) 
VALUES 
    (1, 20.00, 2),
    (2, 50.00, 4);

-- Populate Users table
INSERT INTO Users (user_id, username, email, pswd, group_id) 
VALUES 
    ('1aaaaa', 'mary', 'mary@gmail.com', 'password1', 1),
    ('2bbbbb', 'john', 'john@gmail.com', 'password2', 1),
    ('3ccccc', 'tom', 'tom@gmail.com', 'password3', 2),
    ('4ddddd', 'sam', 'sam@gmail.com', 'password4', 2),
	('5eeeee', 'joe', 'joe@gmail.com', 'password5', 2),
	('6fffff', 'kate', 'kate@gmail.com', 'password6', 2);

-- Populate Transactions table
INSERT INTO Transactions (transaction_id, total_amount, user_id, group_id, discounts_used) 
VALUES 
    (1, 20.00,'1aaaaa', 1, 5.00),
    (2, 30.00,'2bbbbb', 2, 10.00);

-- Populate Catalogue table
INSERT INTO Catalogue (item_id, item_name, item_price) 
VALUES 
    (101, 'Tea', 2.00),
    (102, 'Coffee', 4.00),
    (103, 'Biscuit', 5.00),
    (104, 'Sandwich', 10.00);

-- Populate Transactions_Details table
INSERT INTO Transactions_Details (transaction_id, item_id, quantity) 
VALUES 
    (1, 104, 1),
    (1, 103, 2),
    (2, 102, 2),
	(2, 101, 1),
	(2, 104, 2);
