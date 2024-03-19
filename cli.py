import requests

BASE_URL = 'http://localhost:5000'  # Update this with your server's URL


def signup():
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")
    full_name = input("Enter full name: ")

    response = requests.post(f"{BASE_URL}/signup", json={"user_name": user_name, "user_password": user_password, "full_name": full_name})
    data = response.json()
    print(data)


def login():
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")

    response = requests.post(f"{BASE_URL}/login", json={"user_name": user_name, "user_password": user_password})
    data = response.json()
    print(data)


def get_menu_items():
    response = requests.get(f"{BASE_URL}/menu")
    menu_items = response.json()
    print(menu_items)


def make_transaction():
    user_id = input("Enter user ID: ")
    items = []

    while True:
        item_id = input("Enter item ID (or type 'done' to finish): ")
        if item_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        items.append({"item_id": int(item_id), "quantity": quantity})

    response = requests.post(f"{BASE_URL}/transaction", json={"user_id": user_id, "items": items})
    data = response.json()
    print(data)


def get_transactions():
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/transaction?user_id={user_id}")
    transactions = response.json()
    print(transactions)


def get_user():
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/user?user_id={user_id}")
    user = response.json()
    print(user)


def main():
    while True:
        print("\nMenu:")
        print("1. Signup")
        print("2. Login")
        print("3. Get Menu Items")
        print("4. Make Transaction")
        print("5. Get Transactions")
        print("6. Get User")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            get_menu_items()
        elif choice == '4':
            make_transaction()
        elif choice == '5':
            get_transactions()
        elif choice == '6':
            get_user()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
