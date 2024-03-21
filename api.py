from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

MAX_GROUP_SIZE = 4
POINTS_PERCENTAGE = 1

# Dummy database
groups = {}
users = {}
menu_items = [
    {"item_id": 1, "name": "Coffee", "price": 2.5},
    {"item_id": 2, "name": "Tea", "price": 2.0},
    {"item_id": 3, "name": "Sandwich", "price": 5.0},
]

transactions = []

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Group signup.
    if data.get('group_name') is not None and data.get('group_location') is not None:
        group_name = data.get('group_name')
        group_location = data.get('group_location')
        group_id = generate_id()
        groups[group_id] = {
            'group_name': group_name,
            'group_location': group_location,
            'users': [],
            'points': 0
        }
        return jsonify({'group_id': group_id})
    
    # User signup.
    if data.get('user_name') is not None and data.get('group_id') is not None:
        user_name = data.get('user_name')
        user_password = data.get('user_password')
        full_name = data.get('full_name')
        group_id = data.get('group_id')

        # Ensure group exists.
        if group_id not in groups:
            return jsonify({'error': 'Group not found'}), 404
        # Ensure group is not full.
        if len(groups[group_id].get('users')) >= MAX_GROUP_SIZE:
            return jsonify({'error': 'Group is full'}), 400
        
        # Add user to group.
        user_id = generate_id()
        groups[group_id].get('users').append(user_id)
        users[user_id] = {
            'user_name': user_name,
            'user_password': user_password,
            'full_name': full_name,
            'group_id': group_id
        }

        return jsonify({'user_id': user_id})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_name = data.get('user_name')
    password = data.get('user_password')

    for user_id, user_data in users.items():
        if user_data['user_name'] == user_name and user_data['user_password'] == password:
            return jsonify({'user_id': user_id})

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/menu', methods=['GET'])
def get_menu_items():
    return jsonify(menu_items)


@app.route('/transaction', methods=['POST'])
def make_transaction():
    data = request.json
    user_id = data.get('user_id')
    items = data.get('items')
    use_points = data.get('use_points')

    # Calculate total cost.
    total_cost = 0
    for item in items:
        for menu_item in menu_items:
            if menu_item['item_id'] == item['item_id']:
                total_cost += menu_item['price'] * item['quantity']
                break

    # Calculate points.
    points = total_cost * (POINTS_PERCENTAGE / 100)
    
    # Spend or earn points.
    group_id = users[user_id].get('group_id')
    if use_points:
        if groups[group_id].get('points') < points:
            return jsonify({'error': 'Not enough points'}), 400
        groups[group_id]['points'] -= points
        total_cost -= points
        transactions.append({'user_id': user_id, 'total_cost': total_cost, 'points': -points})
        return jsonify({'total_cost': total_cost, 'points': -points})
    
    groups[group_id]['points'] += points
    transactions.append({'user_id': user_id, 'total_cost': total_cost, 'points': points})
    return jsonify({'total_cost': total_cost, 'points': points})


@app.route('/transaction', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    user_transactions = [transaction for transaction in transactions if transaction['user_id'] == user_id]
    return jsonify(user_transactions)

@app.route('/group', methods=['GET'])
def get_group():
    group_id = request.args.get('group_id')
    group = groups.get(group_id)
    if group:
        return jsonify(group)
    else:
        return jsonify({'error': 'Group not found'}), 404

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
