import mysql.connector
from mysql.connector import Error
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

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
        logger.info("Query executed successfully")
    except Error as e:
        logger.error(f"Error executing query: {e}")

# CRUD methods
# Create
def create_record(connection, table, columns, values):
    """
    DB writes
    """
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
    logger.info(f"  Create query: {query}")
    logger.info(f"  Create values: {values}")
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
        logger.info(f"  Read query: {query}")
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            logger.info(f"  Read record: {record}")
        return records
    except Error as e:
        logger.error(f"Error reading records: {e}")

# def read_all_records(connection, table, condition=None):

# Update
def update_record(connection, table, set_values, condition):
    """
    DB update
    """
    query = f"UPDATE {table} SET {', '.join([f'{col} = %s' for col in set_values.keys()])} WHERE {condition}"
    values = list(set_values.values())
    logger.info(f"  Update query: {query}")
    logger.info(f"  Update values: {values}")
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

        # Construct the UPDATE query
        update_query = f"UPDATE {table} SET {', '.join([f'{col} = %s' for col in set_values.keys()])} WHERE {condition}"
        
        # Extract values from set_values dictionary to pass as parameters
        values = list(set_values.values())

        # Execute the SELECT query with locking
        cursor.execute(f"SELECT * FROM {table} WHERE {condition} FOR UPDATE")

        # Fetch the result set to consume it
        cursor.fetchall()

        # Execute the UPDATE query
        cursor.execute(update_query, values)
        
        # Commit the transaction
        connection.commit()
        logger.info("Transaction committed successfully")
        return True
    except mysql.connector.Error as e:
        # Rollback the transaction if an error occurs
        logger.error(f"Error updating record: {e}")
        connection.rollback()
        return False
    finally:
        # Close the cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
