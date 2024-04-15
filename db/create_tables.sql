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

create table user_groups (
	group_id char(10) NOT NULL,
	discount_points decimal(10, 4) NOT NULL,
	number_members int NOT NULL,
	PRIMARY KEY (group_id)
);

create table users (
	user_id char(10) NOT NULL,
	username varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	pswd varchar(255) NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE group_members (
    group_id char(10),
    user_id char(10),
    FOREIGN KEY (group_id) REFERENCES user_groups(group_id),
    PRIMARY KEY (group_id, user_id)
);

create table transactions (
	transaction_id int NOT NULL,
	total_amount decimal NOT NULL,
	user_id char(10) NOT NULL,
	group_id char(10) NOT NULL,
	discounts_used decimal(10, 4) NOT NULL,
	PRIMARY KEY (transaction_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

create table catalogue (
	item_id int NOT NULL,
	item_name varchar(255) NOT NULL,
	item_price decimal NOT NULL,
	PRIMARY KEY (item_id)
);

create table transactions_details (
	transaction_id int NOT NULL,
	item_id int NOT NULL,
	quantity int NOT NULL,
	FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
	FOREIGN KEY (item_id) REFERENCES catalogue(item_id)
);
