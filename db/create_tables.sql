-- Database: global_cafe

-- DROP DATABASE IF EXISTS global_cafe;

-- CREATE DATABASE global_cafe
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'English_United Kingdom.1252'
--     LC_CTYPE = 'English_United Kingdom.1252'
--     LOCALE_PROVIDER = 'libc'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;

create table User_Groups (
	group_id int NOT NULL,
	discount_points decimal NOT NULL,
	number_members int NOT NULL,
	PRIMARY KEY (group_id)
);

create table Users (
	user_id char(10) NOT NULL,
	username varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	pswd varchar(255) NOT NULL,
	group_id int,
	FOREIGN KEY (group_id) REFERENCES User_Groups(group_id),
	PRIMARY KEY (user_id)
);

CREATE TABLE Group_Members (
    group_id int,
    user_id char(10),
    FOREIGN KEY (group_id) REFERENCES User_Groups(group_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    PRIMARY KEY (group_id, user_id)
);

create table Transactions (
	transaction_id int NOT NULL,
	total_amount decimal NOT NULL,
	user_id char(10) NOT NULL,
	group_id int NOT NULL,
	discounts_used decimal NOT NULL,
	PRIMARY KEY (transaction_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (group_id) REFERENCES User_Groups(group_id)
);

create table Catalogue (
	item_id int NOT NULL,
	item_name varchar(255) NOT NULL,
	item_price decimal NOT NULL,
	PRIMARY KEY (item_id)
);

create table Transactions_Details (
	transaction_id int NOT NULL,
	item_id int NOT NULL,
	quantity int NOT NULL,
	FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
	FOREIGN KEY (item_id) REFERENCES Catalogue(item_id)
);

