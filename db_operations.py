import psycopg2
from psycopg2 import Error

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
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            print(record)
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
    execute_query(connection, query, values)

# Delete
def delete_record(connection, table, condition):
    """
    DB delete
    """
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_query(connection, query)
    