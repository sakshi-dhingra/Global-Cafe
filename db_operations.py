import mysql.connector
from mysql.connector import Error

def execute_query(connection, query, values=None):
    """
    Query execution    
    """
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print("Error executing query:", e)

# CRUD methods
# Create
def create_record(connection, table, columns, values):
    """
    DB writes
    """
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
    print("  Create query:", query)
    print("  Create values:", values)
    execute_query(connection, query, values)

# Read
def read_record(connection, table, condition=None):
    """
    DB reading
    """
    query = f"SELECT * FROM {table}"
    if condition:
        query += f" WHERE {condition}"
    try:
        print("  Read query:", query)
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            print("  Read record:", record)
        return records
    except Error as e:
        print("Error reading records:", e)

# def read_all_records(connection, table, condition=None):

# Update
def update_record(connection, table, set_values, condition):
    """
    DB update
    """
    query = f"UPDATE {table} SET {', '.join([f'{col} = %s' for col in set_values.keys()])} WHERE {condition}"
    values = list(set_values.values())
    print("  Update query:", query)
    print("  Update values:", values)
    execute_query(connection, query, values)

# Delete
def delete_record(connection, table, condition):
    """
    DB delete
    """
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_query(connection, query)


def update_record_transaction(connection, table, set_values, condition):
    """
    Update records in the database table within a transaction
    """
    try:
        # Start the transaction
        cursor = connection.cursor()
        cursor.execute("START TRANSACTION ISOLATION LEVEL SERIALIZABLE;")

        # Construct the UPDATE query
        update_query = f"UPDATE {table} SET {', '.join([f'{col} = %s' for col in set_values.keys()])} WHERE {condition}"
        
        # Extract values from set_values dictionary to pass as parameters
        values = list(set_values.values())

        # Execute the UPDATE query
        cursor.execute(update_query, values)
        
        # Commit the transaction
        connection.commit()
        print("Transaction committed successfully")
        return True
    except mysql.connector.Error as e:
        # Rollback the transaction if an error occurs
        print("Error updating record:", e)
        connection.rollback()
        return False
    finally:
        # Close the cursor
        cursor.close()
