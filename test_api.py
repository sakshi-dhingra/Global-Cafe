"""
Tests for Flask API server. 

Testing for routing
"""
import psycopg2
import mysql.connector

def test_nothing():
    """
    Dummy test.
    """
    assert True

def get_db_connection(region):
    """
    Get db details
    """
    if region.lower() == "ireland": #R1
        return {
            "load_balancer": {"host": "18.201.146.92", "port": 4006},
            "master": {"host": "18.201.146.92", "port": 3307},
            "slave": {"host": "18.201.146.92", "port": 3307}
        }
    elif region.lower() == "us east": #R2
        return {
            "load_balancer": {"host": "54.172.222.222", "port": 4006},
            "master": {"host": "54.172.222.222", "port": 3307},
            "slave": {"host": "54.172.222.222", "port": 3307}
        }
    elif region.lower() == "singapore": #R3
        return {
            "load_balancer": {"host": "18.141.160.15", "port": 4006},
            "master": {"host": "18.141.160.15", "port": 3307},
            "slave": {"host": "18.141.160.15", "port": 3307}
        }
    else:
        raise ValueError("Invalid region")

def connect_to_database(region, db_type):
    """
    Create db connection
    """
    connection_details = get_db_connection(region)
    db_info = connection_details[db_type.lower()]
    
    return mysql.connector.connect(
        host=db_info["host"],
        port=db_info["port"],
        user="admin",
        password="DIstP@assW*rD",
        database="mysql"
    )

# Execute a read query example
def execute_read_query(connection, query):
    """
    run sample read
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def get_table_list(connection):
    """
    Retrieve a list of tables in the database
    """
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        return table_list
    except mysql.connector.Error as e:
        print(f"Error retrieving table list: {e}")
        return None
    finally:
        cursor.close()

def create_tables(connection):
    """
    create sample table
    """
    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS User_Groups")
        connection.commit()
        cursor.execute("""
            create table User_Groups (
	    group_id char(10) NOT NULL,
	    discount_points decimal NOT NULL,
	    number_members int NOT NULL,
	    PRIMARY KEY (group_id));
        """)

        cursor.execute("""
            create table Users (
	user_id char(10) NOT NULL,
	username varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	pswd varchar(255) NOT NULL,
	group_id char(10),
	FOREIGN KEY (group_id) REFERENCES User_Groups(group_id),
	PRIMARY KEY (user_id)
);
        """)

        cursor.execute("""
            CREATE TABLE Group_Members (
    group_id char(10),
    user_id char(10),
    FOREIGN KEY (group_id) REFERENCES User_Groups(group_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    PRIMARY KEY (group_id, user_id)
);
        """)

        cursor.execute("""
            create table Transactions (
	transaction_id int NOT NULL,
	total_amount decimal NOT NULL,
	user_id char(10) NOT NULL,
	group_id char(10) NOT NULL,
	discounts_used decimal NOT NULL,
	PRIMARY KEY (transaction_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (group_id) REFERENCES User_Groups(group_id)
);
        """)

        cursor.execute("""
            create table Catalogue (
	item_id int NOT NULL,
	item_name varchar(255) NOT NULL,
	item_price decimal NOT NULL,
	PRIMARY KEY (item_id)
);
        """)

        cursor.execute("""
            create table Transactions_Details (
	transaction_id int NOT NULL,
	item_id int NOT NULL,
	quantity int NOT NULL,
	FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
	FOREIGN KEY (item_id) REFERENCES Catalogue(item_id)
);
        """)


        connection.commit()
        print("Table 'User_Groups' created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def main():
    """
    main
    """
    # Example usage:
    region = "us east"
    db_type = "load_balancer"
    connection = connect_to_database(region, db_type)
    #create_tables(connection)
    #x = get_table_list(connection)
    #for y in x:
    #    print(y)
    # Example read query
    query = "SELECT * FROM User_Groups LIMIT 10;"
    result = execute_read_query(connection, query)

    if result:
        print("Query result:")
        for row in result:
            print(row)
    else:
        print("No results returned.")

main()
