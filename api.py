"""
Flask API server for the cafe loyalty card system.
"""
import random
import string
import mysql.connector
from flask import Flask, request, jsonify
import mysql.connector
import db_operations as db
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if len(sys.argv) < 3:
    logger.error("Please pass home region of server and port")
    exit()

app = Flask(__name__)

MAX_GROUP_SIZE = 4
POINTS_PERCENTAGE = 10
HOME_REGION = sys.argv[1]
PORT = sys.argv[2]


def get_db_connection(region):
    """
    Get db details based on region
    """
    if region.lower() == "r1" or region == "001":  # R1 Ireland
        return {
            "load_balancer": {"host": "18.201.52.2", "port": 4006},
            "master": {"host": "18.201.52.2", "port": 3307},
            "slave": {"host": "18.201.52.2", "port": 3307}
        }
    elif region.lower() == "r2" or region == "002":  # R2 US East
        return {
            "load_balancer": {"host": "54.196.146.52", "port": 4006},
            "master": {"host": "54.196.146.52", "port": 3307},
            "slave": {"host": "54.196.146.52", "port": 3307}
        }
    elif region.lower() == "r3" or region == "003":  # R3 Singapore
        return {
            "load_balancer": {"host": "18.136.103.207", "port": 4006},
            "master": {"host": "18.136.103.207", "port": 3307},
            "slave": {"host": "18.136.103.207", "port": 3307}
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
        database="global_cafe"
    )


def generate_id():
    """
    Generate a random ID.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))


@app.route('/signup/group', methods=['POST'])
def group_sign_up():
    """
    Group signup method
    """

    region = request.args.get('region')
    conn = connect_to_database(region, "load_balancer")
    
    # generate prefix
    region = region.lower()
    if region == 'r1':
        region = "001-"
    elif region == 'r2':
        region = "002-"
    elif region == 'r3':
        region = "003-"
    else:
        region = "001-"
    
    # generate group id
    group_id = f'{region}g{generate_id()}'
    
    # insert into DB
    values = [str(group_id), '0', '0']
    columns = ["group_id", "discount_points", "number_members"]
    db.create_record(conn, 'user_groups', columns, values)
    return jsonify({'group_id': group_id})


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

        region_group = group_id[:3]

        conn_group = connect_to_database(region_group, "load_balancer")
        groups = db.read_record(
            conn_group, "user_groups", f"group_id='{group_id}'")
        # print(groups)
        # Ensure group exists.
        if len(groups) == 0:
            return jsonify({'error': 'Group not found'}), 404
        # Ensure group is not full.
        if groups[0][2] >= MAX_GROUP_SIZE:
            return jsonify({'error': 'Group is full'}), 400

        # generate user id prefix
        location = location.lower()
        if location == 'r1':
            location = "001-"
        elif location == 'r2':
            location = "002-"
        elif location == 'r3':
            location = "003-"
        else:
            location = "001-"
        # generate user id
        user_id = f'{location}u{generate_id()}'

        # User group tally updated
        updated_group_members = {"number_members": int(groups[0][2]) + 1}
        db.update_record(conn_group, "user_groups",
                         updated_group_members, f"group_id='{group_id}'")

        # Create user
        columns = ["user_id", "username", "email", "pswd"]
        values = [user_id, user_name, email, user_password]
        region_user = user_id[:3]
        conn_user = connect_to_database(region_user, "load_balancer")
        db.create_record(conn_user, "users", columns, values)

        # Update group_members table
        columns = ["group_id", "user_id"]
        values = [group_id, user_id]
        db.create_record(conn_group, "group_members", columns, values)

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

        region_group = group_id[:3]
        region_user = user_id[:3]

        conn_group = connect_to_database(region_group, "load_balancer")

        groups = db.read_record(
            conn_group, "user_groups", f"group_id='{group_id}'")
        if len(groups) == 0:
            return jsonify({'error': 'Group not found'}), 404

        conn_user = connect_to_database(region_user, "load_balancer")
        users = db.read_record(conn_user, "users", f"user_id='{user_id}'")
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

        # User group tally updated
        updated_group_members = {"number_members": int(groups[0][2]) + 1}
        db.update_record(conn_group, "user_groups",
                         updated_group_members, f"group_id='{group_id}'")

        # Update group_members table
        columns = ["group_id", "user_id"]
        values = [group_id, user_id]
        db.create_record(conn_group, "group_members", columns, values)

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
    region = data.get('region')
    conn_user = connect_to_database(region, "load_balancer")

    user = db.read_record(conn_user, "users", "'" + user_name +
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
    conn = connect_to_database(HOME_REGION, "load_balancer")
    menu_items = db.read_record(conn, "catalogue")
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
    region_user = user_id[:3]
    region_group = group_id[:3]

    if region_user == region_group:
        same_region = True
        conn = connect_to_database(region_user, "load_balancer")
    else:
        same_region = False
        conn = None
        conn_user = connect_to_database(region_user, "load_balancer")
        conn_group = connect_to_database(region_group, "load_balancer")

    # get menu items
    conn_menu = connect_to_database(HOME_REGION, "load_balancer")
    menu_items = db.read_record(conn_menu, "catalogue")

    if same_region:
        user = db.read_record(conn, "users", f"user_id='{user_id}'")
        groups = db.read_record(conn, "group_members",
                                f"user_id='{user_id}' AND group_id='{group_id}'")
    else:
        user = db.read_record(conn_user, "users", f"user_id='{user_id}'")
        groups = db.read_record(conn_group, "group_members",
                                f"user_id='{user_id}' AND group_id='{group_id}'")
    if not groups:
        return jsonify({'error': f'User {user_id} not in group {group_id}'}), 401

    if same_region:
        user_group = db.read_record(
            conn, "user_groups", f"group_id='{group_id}'")
        highest = db.read_record(
            conn, "transactions", "transaction_id = (SELECT MAX(transaction_id) FROM transactions);")
    else:
        user_group = db.read_record(
            conn_group, "user_groups", f"group_id='{group_id}'")
        highest = db.read_record(
            conn_user, "transactions", "transaction_id = (SELECT MAX(transaction_id) FROM transactions);")

    if highest is not None and len(highest) > 0 and highest[0] is not None:
        high_id = highest[0][0] + 1
    else:
        high_id = 1
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
        new_points_total = {"discount_points": group_points}

        if same_region:
            res = db.update_record_transaction(conn, "user_groups", new_points_total,
                              f"group_id='{group_id}'")
            if res:
                db.create_record(conn, "transactions", columns, values)
            else:
                return jsonify({"message": "Unable to modify group points."}), 500
        else:
            
            res = db.update_record_transaction(conn_group, "user_groups", new_points_total,
                              f"group_id='{group_id}'")
            if res:
                db.create_record(conn_user, "transactions", columns, values)
            else:
                return jsonify({"message": "Unable to modify group points."}), 500

        return jsonify({'total_cost': total_cost, 'points': -use_points})
    # points awarded if not redeeming
    else:
        # Calculate points.
        points = total_cost * (POINTS_PERCENTAGE / 100)
        new_points = float(points + group_points)
        
        new_points_total = {"discount_points": new_points}
        
        columns = ['transaction_id', 'total_amount',
                   'user_id', 'group_id', 'discounts_used']
        values = [high_id, total_cost, user[0][0], group_id, 0]

        if same_region:
            res = db.update_record_transaction(conn, "user_groups", new_points_total,
                              f"group_id='{group_id}'")
            if res:
                db.create_record(conn, "transactions", columns, values)
            else:
                return jsonify({"message": "Unable to modify group points."}), 500
        else:
            res = db.update_record_transaction(conn_group, "user_groups", new_points_total,
                              f"group_id='{group_id}'")
            if res:
                db.create_record(conn_user, "transactions", columns, values)
            else:
                return jsonify({"message": "Unable to modify group points."}), 500
        return jsonify({'total_cost': total_cost, 'points': points})


@app.route('/transaction', methods=['GET'])
def get_transactions():
    """
    Get transactions by user ID.
    """
    user_id = request.args.get('user_id')
    region = user_id[:3]
    conn = connect_to_database(region, "load_balancer")

    transactions = db.read_record(
        conn, "transactions", "'" + user_id + "' = user_id")
    return jsonify(transactions)


@app.route('/group', methods=['GET'])
def get_group():
    """
    Get group details by group ID.
    """
    group_id = request.args.get('group_id')
    region = group_id[:3]
    conn = connect_to_database(region, "load_balancer")
    group = db.read_record(conn, "user_groups", "'" +
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
    region = user_id[:3]
    conn = connect_to_database(region, "load_balancer")

    user = db.read_record(conn, "users", "'" + user_id + "' = user_id")
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "all good"})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=PORT)
