from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Dummy database
users = {}
menu_items = [
    {"item_id": 1, "name": "Coffee", "price": 2.5},
    {"item_id": 2, "name": "Tea", "price": 2.0},
    {"item_id": 3, "name": "Sandwich", "price": 5.0},
]

transactions = []


def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user_name = data.get('user_name')
    user_password = data.get('user_password')
    full_name = data.get('full_name')

    user_id = generate_user_id()
    users[user_id] = {
        'user_name': user_name,
        'user_password': user_password,
        'full_name': full_name
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

    total_cost = 0
    for item in items:
        for menu_item in menu_items:
            if menu_item['item_id'] == item['item_id']:
                total_cost += menu_item['price'] * item['quantity']
                break

    discount_points = total_cost * 0.01
    transactions.append({'user_id': user_id, 'total_cost': total_cost, 'discount_points': discount_points})

    return jsonify({'total_cost': total_cost, 'discount_points': discount_points})


@app.route('/transaction', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    user_transactions = [transaction for transaction in transactions if transaction['user_id'] == user_id]
    return jsonify(user_transactions)


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
