SELECT u.username, u.email, g.discount_points
FROM Users u
JOIN User_Groups g ON u.group_id = g.group_id
WHERE u.group_id = 1; 

SELECT u.username AS user_name, t.transaction_id, c.item_name, td.quantity
FROM Users u
JOIN Transactions t ON u.user_id = t.user_id
JOIN Transactions_Details td ON t.transaction_id = td.transaction_id
JOIN Catalogue c ON td.item_id = c.item_id;
