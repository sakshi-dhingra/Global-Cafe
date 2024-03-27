"""
Flask API server for the cafe loyalty card system.
"""
import random
import string
import psycopg2
import db_operations as db

from flask import Flask, request, jsonify

app = Flask(__name__)

# 4
MAX_GROUP_SIZE = 10000
POINTS_PERCENTAGE = 1

def connectToDB():
    try:
        connection = psycopg2.connect(host="localhost", port="5432", database="global_cafe", user="davidburton", password="")
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
def groupSignUp():
    highest = db.read_record(conn, "user_groups", "group_id = (SELECT MAX(group_id) FROM user_groups);")
    columns = ["group_id", "discount_points", "number_members"]
    highId = highest[0][0] + 1
    values = [str(highId), '0', '0']
    db.create_record(conn, 'user_groups', columns, values)
                     
    return jsonify({'Success':f'Group Created with id {highId}.'})

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
        groups = db.read_record(conn, "user_groups", "'" + group_id + "' = group_id") 

        # Ensure group exists.
        if int(group_id) is not int(groups[0][0]):
            print(group_id)
            print(groups[0][0])
            return jsonify({'error': 'Group not found'}), 404
        # Ensure group is not full.
        if groups[0][2] >= MAX_GROUP_SIZE:
            return jsonify({'error': 'Group is full'}), 400

        user_id = generate_id()
        updated_group_members = {"number_members": int(groups[0][2]) + 1}

        # User group tally updated
        db.update_record(conn, "User_Groups", updated_group_members, "'" + group_id + "' = group_id")

        # Create user
        columns = ["user_id", "username", "email", "pswd", "group_id"]
        values = [user_id, user_name, email, user_password, group_id]
        db.create_record(conn, "Users", columns, values)

        return jsonify({'user_id': user_id})
    return jsonify({'error': 'Invalid data'}), 400


@app.route('/login', methods=['POST'])
def login():
    """
    Login as user.
    """
    data = request.json
    user_name = data.get('user_name')
    password = data.get('user_password')

    user = db.read_record(conn, "Users", "'" + user_name + "' = username AND pswd = '" + password + "'" )
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
    items = data.get('items')
    use_points = data.get('use_points')

    # Calculate total cost.
    total_cost = 0

    # call db - get menu_items
    for item in items:
        for menu_item in menu_items:
            if menu_item['item_id'] == item['item_id']:
                total_cost += menu_item['price'] * item['quantity']
                break

<<<<<<< HEAD
=======
    # Calculate points.
    points = total_cost * (POINTS_PERCENTAGE / 100)

    # call db - get users, groups
    # call db - post transactions
>>>>>>> 8107e0f (Added in CRUD operations)
    # Spend or earn points.
    group_id = users[user_id].get('group_id')
    
    # no new points awarded when redeeming points
    if use_points:
        if groups[group_id].get('points') < use_points:
            return jsonify({'error': 'Not enough points'}), 400
        groups[group_id]['points'] -= use_points
        total_cost -= use_points
        transactions.append({'user_id': user_id, 'total_cost': total_cost, 'points': -use_points})
        return jsonify({'total_cost': total_cost, 'points': -use_points})
    
    # points awarded if not redeeming
    else:
        # Calculate points.
        points = total_cost * (POINTS_PERCENTAGE / 100)

        groups[group_id]['points'] += points
        transactions.append({'user_id': user_id, 'total_cost': total_cost, 'points': points})
        return jsonify({'total_cost': total_cost, 'points': points})


@app.route('/transaction', methods=['GET'])
def get_transactions():
    """
    Get transactions by user ID.
    """
    user_id = request.args.get('user_id')

    transactions = db.read_record(conn, "Transactions", "'" + user_id + "' = user_id")
    return jsonify(transactions)


@app.route('/group', methods=['GET'])
def get_group():
    """
    Get group details by group ID.
    """
    group_id = request.args.get('group_id')
    group = db.read_record(conn, "User_groups", "'" + group_id + "' = group_id")
    if group:
        return jsonify(group)
    return jsonify({'error': 'Group not found'}), 404


@app.route('/user', methods=['GET'])
def get_user():
    """
    Get user details by user ID.
    """
    user_id = request.args.get('user_id')

    user = db.read_record(conn, "Users", "'" + user_id + "' = user_id")
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    conn = connectToDB()
    app.run(debug=True)
