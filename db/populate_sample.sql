-- Database: global_cafe

-- Populate user_groups table
INSERT INTO user_groups (group_id, discount_points, number_members) 
VALUES 
    (1, 20.00, 2),
    (2, 50.00, 4);

-- Populate users table
INSERT INTO users (user_id, username, email, pswd, group_id) 
VALUES 
    ('001-1aaaaa', 'mary', 'mary@gmail.com', 'password1', 1),
    ('002-2bbbbb', 'john', 'john@gmail.com', 'password2', 1),
    ('001-3ccccc', 'tom', 'tom@gmail.com', 'password3', 2),
    ('003-4ddddd', 'sam', 'sam@gmail.com', 'password4', 2),
	('002-5eeeee', 'joe', 'joe@gmail.com', 'password5', 2),
	('001-6fffff', 'kate', 'kate@gmail.com', 'password6', 2);

-- Populate group_members table
INSERT INTO group_members (group_id, user_id)
VALUES
    (1, '001-1aaaaa'),
    (1, '002-2bbbbb'),
    (2, '001-3ccccc'),
    (2, '003-4ddddd'),
	(2, '002-5eeeee'),
	(2, '001-6fffff');

-- Populate transactions table
INSERT INTO transactions (transaction_id, total_amount, user_id, group_id, discounts_used) 
VALUES 
    (1, 20.00,'001-1aaaaa', 1, 5.00),
    (2, 30.00,'002-2bbbbb', 2, 10.00);

-- Populate catalogue table
INSERT INTO catalogue (item_id, item_name, item_price) 
VALUES 
    (101, 'Tea', 2.00),
    (102, 'Coffee', 4.00),
    (103, 'Biscuit', 5.00),
    (104, 'Sandwich', 10.00);

-- Populate transactions_details table
INSERT INTO transactions_details (transaction_id, item_id, quantity) 
VALUES 
    (1, 104, 1),
    (1, 103, 2),
    (2, 102, 2),
	(2, 101, 1),
	(2, 104, 2);
