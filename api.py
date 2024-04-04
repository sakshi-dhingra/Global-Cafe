"""
Flask API server for the cafe loyalty card system.
"""
import random
import string
import psycopg2
from flask import Flask, request, jsonify
import mysql.connector
import db_operations as db

app = Flask(__name__)

MAX_GROUP_SIZE = 4
POINTS_PERCENTAGE = 1


def get_db_connection(region):
    """
    Get db details based on region
    """
    if region.lower() == "r1" or region == "001":  # R1 Ireland
        return {
            "load_balancer": {"host": "18.201.146.92", "port": 4006},
            "master": {"host": "18.201.146.92", "port": 3307},
            "slave": {"host": "18.201.146.92", "port": 3307}
        }
    elif region.lower() == "r2" or region == "002":  # R2 US East
        return {
            "load_balancer": {"host": "54.172.222.222", "port": 4006},
            "master": {"host": "54.172.222.222", "port": 3307},
            "slave": {"host": "54.172.222.222", "port": 3307}
        }
    elif region.lower() == "r3" or region == "003":  # R3 Singapore
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


def connect_to_db(host, port, database, user, password):
    """
    Create db connection
    """
    try:
        connection = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password)
        print("Connected to the database")
        return connection
    except Exception as e:
        print("Error: ", e)


def generate_id():
    """
    Generate a random ID.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/signup/group', methods=['POST'])
def group_sign_up():
    """
    Group signup method
    """

    region = request.args.get('region')
    # conn = connect_to_database(region, "load_balancer")
    #highest=db.read_record(conn, "user_groups","group_id=(SELECT MAX(group_id) FROM user_groups);")
    columns = ["group_id", "discount_points", "number_members"]
    # high_id = highest[0][0] + 1
    region = region.lower()
    if region == 'r1':
        region = "001-"
    elif region == 'r2':
        region = "002-"
    elif region == 'r3':
        region = "003-"
    else:
        region = "001-"

    high_id = f'{region}{generate_id()}'
    values = [str(high_id), '0', '0']
    db.create_record(conn, 'user_groups', columns, values)
    return jsonify({'group_id': high_id})


@app.route('/signup', methods=['POST'])
def signup():
    """
    Signup as user or group.
    """
    data = request.json

    if data.get('user_name') is not None and data.get('group_id') is not None:

        user_name = data.get('user_name')
        user_password = data.get('user_password')
        group_id = data.get('group_id')
        email = data.get('email')
        location = data.get('location')

        #region = group_id[:3]
        # conn = connect_to_database(data.get('location'), "load_balancer")
        # conn = connect_to_database(region), "load_balancer")
        groups = db.read_record(conn, "user_groups", f"group_id='{group_id}'")
        # print(groups)
        # Ensure group exists.
        if group_id not in groups[0]:
            print(group_id)
            print(groups[0][0])
            return jsonify({'error': 'Group not found'}), 404
        # Ensure group is not full.
        if groups[0][2] >= MAX_GROUP_SIZE:
            return jsonify({'error': 'Group is full'}), 400

        location = location.lower()
        if location == 'r1':
            location = "001-"
        elif location == 'r2':
            location = "002-"
        elif location == 'r3':
            location = "003-"
        else:
            location = "001-"

        user_id = f'{location}{generate_id()}'
        updated_group_members = {"number_members": int(groups[0][2]) + 1}

        # User group tally updated
        db.update_record(conn, "user_groups",
                         updated_group_members, f"group_id='{group_id}'")

        # Create user
        columns = ["user_id", "username", "email", "pswd", "group_id"]
        values = [user_id, user_name, email, user_password, group_id]
        db.create_record(conn, "Users", columns, values)

        # Update group_members table
        columns = ["group_id", "user_id"]
        values = [group_id, user_id]
        db.create_record(conn, "Group_Members", columns, values)

        return jsonify({'user_id': user_id})
    return jsonify({'error': 'Invalid data'}), 400


@app.route('/join_group', methods=['POST'])
def join_group():
    """
    Join a group.
    """
    data = request.json

    if data.get('user_id') is not None and data.get('group_id') is not None:

        group_id = data.get('group_id')
        user_id = data.get('user_id')

        #region = group_id[:3]
        # conn = connect_to_database(user_id[:3], "load_balancer")
        # conn = connect_to_database(region), "load_balancer")

        groups = db.read_record(conn, "user_groups", f"group_id='{group_id}'")
        if len(groups) == 0:
            return jsonify({'error': 'Group not found'}), 404
        users = db.read_record(conn, "users", f"user_id='{user_id}'")
        if len(users) == 0:
            return jsonify({'error': 'User not found'}), 404

        # Ensure user exists.
        if user_id != users[0][0]:
            print(user_id)
            print(users[0][0])
            return jsonify({'error': 'User not found'}), 404

        # Ensure group exists.
        if group_id not in groups[0]:
            print(group_id)
            print(groups[0][0])
            return jsonify({'error': 'Group not found'}), 404
        # Ensure group is not full.
        if groups[0][2] >= MAX_GROUP_SIZE:
            return jsonify({'error': 'Group is full'}), 400

        updated_group_members = {"number_members": int(groups[0][2]) + 1}

        # User group tally updated
        db.update_record(conn, "User_Groups",
                         updated_group_members, f"group_id='{group_id}'")

        # Update group_members table
        columns = ["group_id", "user_id"]
        values = [group_id, user_id]
        db.create_record(conn, "Group_Members", columns, values)

        return jsonify({'user_id': user_id, 'group_id': group_id})
    return jsonify({'error': 'Invalid data'}), 400


@app.route('/login', methods=['POST'])
def login():
    """
    Login as user.
    """
    data = request.json
    user_name = data.get('user_name')
    password = data.get('user_password')
    #region = data.get('region')
    # conn = connect_to_database(data.get('region'), "load_balancer")

    user = db.read_record(conn, "Users", "'" + user_name +
                          "' = username AND pswd = '" + password + "'")
    user_id_db = user[0][0]
    user_name_db = user[0][1]
    user_password_db = user[0][3]

    if user_name_db == user_name and user_password_db == password:
        return jsonify({'user_id': user_id_db})

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/menu', methods=['GET'])
def get_menu_items():
    """
    Get menu items.
    """
    menu_items = db.read_record(conn, "Catalogue")
    return jsonify(menu_items)


@app.route('/transaction', methods=['POST'])
def make_transaction():
    """
    Make a transaction.
    """
    data = request.json
    user_id = data.get('user_id')
    group_id = data.get('group_id')
    items = data.get('items')
    use_points = data.get('use_points')

    #region = user_id[:3]
    # region = group_id[:3]
    # conn = connect_to_database(region, "load_balancer")

    menu_items = db.read_record(conn, "Catalogue")
    user = db.read_record(conn, "users", f"user_id='{user_id}'")
    groups = db.read_record(conn, "group_members",
                            f"user_id='{user_id}' AND group_id='{group_id}'")
    if not groups:
        return jsonify({'error': f'User {user_id} not in group {group_id}'}), 401

    user_group = db.read_record(conn, "user_groups", f"group_id='{group_id}'")
    highest = db.read_record(
        conn, "transactions", "transaction_id = (SELECT MAX(transaction_id) FROM transactions);")
    high_id = highest[0][0] + 1
    group_points = float(user_group[0][1])

    menu_items_use = [(t[0], float(t[2])) for t in menu_items]

    # Calculate total cost.
    total_cost = 0.0

    for item in items:
        for menu_item in menu_items_use:
            if menu_item[0] == item['item_id']:
                total_cost += menu_item[1] * float(item['quantity'])

    # Spend or earn points.
    # no new points awarded when redeeming points
    if use_points:
        if group_points < use_points:
            return jsonify({'error': 'Not enough points'}), 400
        group_points -= use_points
        total_cost -= use_points
        columns = ['transaction_id', 'total_amount',
                   'user_id', 'group_id', 'discounts_used']
        values = [high_id, total_cost, user[0][0], group_id, -use_points]
        db.create_record(conn, "transactions", columns, values)
        new_points_total = {"discount_points": group_points}
        db.update_record(conn, "user_groups", new_points_total,
                         "'" + str(group_id) + "' = group_id")

        return jsonify({'total_cost': total_cost, 'points': -use_points})
    # points awarded if not redeeming
    else:
        # Calculate points.
        points = total_cost * (POINTS_PERCENTAGE / 100)
        new_points = points + group_points
        new_points_total = {"discount_points": new_points}
        db.update_record(conn, "user_groups", new_points_total,
                         "'" + str(group_id) + "' = group_id")

        columns = ['transaction_id', 'total_amount',
                   'user_id', 'group_id', 'discounts_used']
        values = [high_id, total_cost, user[0][0], group_id, 0]
        db.create_record(conn, "transactions", columns, values)

        return jsonify({'total_cost': total_cost, 'points': points})


@app.route('/transaction', methods=['GET'])
def get_transactions():
    """
    Get transactions by user ID.
    """
    user_id = request.args.get('user_id')
    #region = user_id[:3]
    # conn = connect_to_database(region, "load_balancer")

    transactions = db.read_record(
        conn, "Transactions", "'" + user_id + "' = user_id")
    return jsonify(transactions)


@app.route('/group', methods=['GET'])
def get_group():
    """
    Get group details by group ID.
    """
    group_id = request.args.get('group_id')
    #region = group_id[:3]
    # conn = connect_to_database(region, "load_balancer")
    group = db.read_record(conn, "User_groups", "'" +
                           group_id + "' = group_id")
    if group:
        return jsonify(group)
    return jsonify({'error': 'Group not found'}), 404


@app.route('/user', methods=['GET'])
def get_user():
    """
    Get user details by user ID.
    """
    user_id = request.args.get('user_id')
    #region = user_id[:3]
    # conn = connect_to_database(region, "load_balancer")

    user = db.read_record(conn, "Users", "'" + user_id + "' = user_id")
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    conn = connect_to_db(host="localhost", port="5432",
                         database="global_cafe", user="postgres", password="postgres")
    # conn = connect_to_database("001", "load_balancer") #default connection to Ireland
    app.run(debug=True)
