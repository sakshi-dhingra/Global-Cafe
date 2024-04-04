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

def create_table(connection):
    """
    create sample table
    """
    cursor = connection.cursor()
    try:
        cursor.execute("""
            create table User_Groups (
	    group_id int NOT NULL,
	    discount_points decimal NOT NULL,
	    number_members int NOT NULL,
	    PRIMARY KEY (group_id));
        """)
        connection.commit()
        print("Table 'User_Groups' created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

#create_table(connection)

def main():
    """
    main
    """
    # Example usage:
    region = "ireland"
    db_type = "load_balancer"
    connection = connect_to_database(region, db_type)
    # Example read query
    query = "SELECT * FROM User_Groups LIMIT 10;"
    result = execute_read_query(connection, query)

    if result:
        print("Query result:")
        for row in result:
            print(row)
    else:
        print("No results returned.")
