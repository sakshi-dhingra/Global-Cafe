"""
Simple CLI for interacting with the server.
"""
import requests

BASE_URL = 'http://localhost:5000'  # Update this with your server's URL

def signup_group():
    """
    Sign-up a group.
    """
    group_name = input("Enter group name: ")
    group_location = input("Enter group location: ")
    response = requests.post(f"{BASE_URL}/signup",
                             json={
                                 "group_name": group_name,
                                 "group_location": group_location
                                 })
    data = response.json()
    print(data)


def signup_user():
    """
    Sign-up a user.
    """
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")
    full_name = input("Enter full name: ")
    group_id = input("Enter group ID: ")

    response = requests.post(f"{BASE_URL}/signup",
                             json={
                                 "user_name": user_name,
                                 "user_password": user_password,
                                 "full_name": full_name,
                                 "group_id": group_id
                                 })
    data = response.json()
    print(data)


def login():
    """
    Login as user.
    """
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")

    response = requests.post(f"{BASE_URL}/login",
                             json={
                                 "user_name": user_name,
                                 "user_password": user_password
                                 })
    data = response.json()
    print(data)


def get_menu_items():
    """
    Get menu items.
    """
    response = requests.get(f"{BASE_URL}/menu")
    menu_items = response.json()
    print(menu_items)


def make_transaction():
    """
    Make a transaction.
    """
    user_id = input("Enter user ID: ")
    items = []

    while True:
        item_id = input("Enter item ID (or type 'done' to finish): ")
        if item_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        items.append({"item_id": int(item_id), "quantity": quantity})
        use_points = float(input("Redeem how many points: "))

    response = requests.post(f"{BASE_URL}/transaction",
                             json={
                                 "user_id": user_id,
                                 "items": items,
                                 "use_points": use_points
                                 })
    data = response.json()
    print(data)


def get_transactions():
    """
    Get transactions for a specified user.
    """
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/transaction?user_id={user_id}")
    transactions = response.json()
    print(transactions)


def get_group():
    """
    Get group details.
    """
    group_id = input("Enter group ID: ")
    response = requests.get(f"{BASE_URL}/group?group_id={group_id}")
    group = response.json()
    print(group)


def get_user():
    """
    Get user details.
    """
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/user?user_id={user_id}")
    user = response.json()
    print(user)


def main():
    """
    Main function.
    """
    while True:
        print("\nMenu:")
        print("1. Signup group")
        print("2. Signup user")
        print("3. Login")
        print("4. Get Menu Items")
        print("5. Make Transaction")
        print("6. Get Transactions")
        print("7. Get Group")
        print("8. Get User")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            signup_group()
        elif choice == '2':
            signup_user()
        elif choice == '3':
            login()
        elif choice == '4':
            get_menu_items()
        elif choice == '5':
            make_transaction()
        elif choice == '6':
            get_transactions()
        elif choice == '7':
            get_group()
        elif choice == '8':
            get_user()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
