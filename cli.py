"""
Simple CLI for interacting with the server.
"""
import random
import time
import requests
from tabulate import tabulate
import sys

if len(sys.argv) < 2:
    print("Please pass server_ip:port")
    exit()

BASE_URL = f'http://{sys.argv[1]}'  # Update this with your server's URL

def signup_group():
    """
    Sign-up a group.
    """
    # group_name = input("Enter group name: ")
    # group_location = input("Enter group location: ")

    region = input("Enter region r1, r2 or r3: ")
    response = requests.post(f"{BASE_URL}/signup/group?region={region}",
                             json={})
    if response.status_code != 200:
        print("Error while creating group:", response.text, response.status_code)
        return
    data = response.json()
    print("Group created with group id:", data["group_id"])
    print()


def signup_user():
    """
    Sign-up a user.
    """
    user_name = input("Enter username: ")
    email = input("Enter email: ")
    user_password = input("Enter password: ")
    full_name = input("Enter full name: ")
    group_id = input("Enter group ID: ")
    location = input("Enter your Home Region (R1, R2 or R3): ")

    response = requests.post(f"{BASE_URL}/signup",
                             json={
                                 "user_name": user_name,
                                 "email": email,
                                 "user_password": user_password,
                                 "full_name": full_name,
                                 "group_id": group_id,
                                 "location": location
                                 })
    if response.status_code != 200:
        print("Error while signup:", response.text, response.status_code)
        return
    data = response.json()
    print("User created with user id: {} and is member of group id: {}\n".format(data["user_id"], group_id))

def join_group():
    """
    Join a group.
    """
    user_id = input("Enter user id: ")
    group_id = input("Enter group id you wish to join: ")
    response = requests.post(f"{BASE_URL}/join_group",
                             json={
                                 "user_id": user_id,
                                 "group_id": group_id
                                 })
    if response.status_code != 200:
        print("Error while joining group:", response.text, response.status_code)
        return
    data = response.json()
    print("User with user id: {} and is now member of group id: {}".format(user_id, group_id))
    print()

def login():
    """
    Login as user.
    """
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")
    user_region = input("Region: ")

    response = requests.post(f"{BASE_URL}/login",
                             json={
                                 "user_name": user_name,
                                 "user_password": user_password,
                                 "region": user_region
                                 })
    if response.status_code != 200:
        print("Error while login:", response.text, response.status_code)
        return
    data = response.json()
    print("Login successful, your user id is", data["user_id"])
    print()


def get_menu_items():
    """
    Get menu items.
    """
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code != 200:
        print("Error while getting menu items:", response.text, response.status_code)
        return
    menu_items = response.json()
    print("\nCafe Menu:")
    print(tabulate(menu_items, headers=["Item ID", "Item Name", "Cost (Euros)"], tablefmt="rounded_outline"))
    print()

def make_transaction():
    """
    Make a transaction.
    """
    user_id = input("Enter user ID: ")
    group_id = input("Enter Group ID: ")
    items = []

    while True:
        item_id = input("Enter item ID (or type 'done' to finish): ")
        if item_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        items.append({"item_id": int(item_id), "quantity": quantity})
    
    print("\nSelected items:")
    print(tabulate(items, headers="keys", tablefmt="rounded_outline"))
    print()

    use_points = float(input("Redeem how many points: "))

    response = requests.post(f"{BASE_URL}/transaction",
                             json={
                                 "user_id": user_id,
                                 "group_id": group_id,
                                 "items": items,
                                 "use_points": use_points
                                 })
    if response.status_code != 200:
        print("Error during transaction:", response.text, response.status_code)
        return
    data = response.json()
    print("Transaction successful with total") # points total_cost
    print("  Total:", data["total_cost"])
    if data["points"] >= 0:
        print("  Points earned:", data["points"])
    else:
        print("  Points spent:", -data["points"])
    print()


def get_transactions():
    """
    Get transactions for a specified user.
    """
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/transaction?user_id={user_id}")
    if response.status_code != 200:
        print("Error when fetching transaction history:", response.text, response.status_code)
        return
    transactions = response.json()
    print("\nTransactions:")
    print(tabulate(transactions, headers=["Transaction ID", "Total Cost (Euros)", "User ID", "Group ID", "Discounts points used"], tablefmt="rounded_outline"))
    print()


def get_group():
    """
    Get group details.
    """
    group_id = input("Enter group ID: ")
    response = requests.get(f"{BASE_URL}/group?group_id={group_id}")
    if response.status_code != 200:
        print("Error when getting group details:", response.text, response.status_code)
        return
    group = response.json()
    print("Group points balance: {}, Group members: {}\n".format(group[0][1], group[0][2]))


def get_user():
    """
    Get user details.
    """
    user_id = input("Enter user ID: ")
    response = requests.get(f"{BASE_URL}/user?user_id={user_id}")
    if response.status_code != 200:
        print("Error when getting user details:", response.text, response.status_code)
        return
    user = response.json()
    #[['001-EMUUyw', 'test', 'test', 'test']]
    print("\nUser details:")
    print("  Username:", user[0][1])
    print("  Email:", user[0][2])
    print()


def run_scenario():
    """
    Run test scenario
    """
    # Create 8 new groups.
    print("--- Create 8 new groups.")
    group_ids = []
    locations = ["r1", "r2", "r3"]
    for _ in range(7):
        response = requests.post(f"{BASE_URL}/signup/group?region={random.choice(locations)}",
                                 json={})
        data = response.json()
        group_ids.append(data['group_id'])
    existing_groups = [i for i in range(group_ids[0])]
    group_ids.extend(existing_groups)

    # Create 20 users (choose random group).
    print("--- Create 20 users (choose random group).")
    names = ["Alice", "Bob", "Charlie", "Dominic", "Eve", "Frank", 
             "Grace", "Heidi", "Ivan", "Judy", "Kevin", 
             "Linda", "Michael", "Nancy", "Oscar", "Peggy", 
             "Quincy", "Rita", "Steve", "Tina", "Ursula"]
    user_groups = {}
    user_ids = []
    while len(user_ids) < 20:
        group_id = group_ids[random.randint(0, len(group_ids) - 1)]
        name = names[0]
        response = requests.post(f"{BASE_URL}/signup",
                                    json={
                                        "user_name": name,
                                        "email": f"{name.lower()}@example.com",
                                        "user_password": f"password{random.randint(1, 1000)}",
                                        "full_name": name,
                                        "location": random.choice(locations),
                                        "group_id": group_id
                                        })
        if response.status_code != 200:
            print(response.text, response.status_code)
        data = response.json()
        if 'user_id' not in data:
            continue
        user_groups[data['user_id']] = [group_id]
        user_ids.append(data['user_id'])
        names.remove(name)

    # Randomly try and join 10 users to groups.
    print("--- Randomly try and join 10 users to groups.")
    for _ in range(10):
        user_id = user_ids[random.randint(0, len(user_ids) - 1)]
        group_id = group_ids[random.randint(0, len(group_ids) - 1)]
        response = requests.post(f"{BASE_URL}/join_group",
                                 json={
                                     "user_id": user_id,
                                     "group_id": group_id
                                     })
        if response.status_code != 200:
            print(response.text, response.status_code)
            continue
        user_groups[user_id].append(group_id)
        data = response.json()
        print(data)

    # Make 200 transactions (choose random user and random items).
    print("--- Make 200 transactions (choose random user and random items).")
    menu_items = requests.get(f"{BASE_URL}/menu").json()
    print(menu_items[0])
    for _ in range(200):
        user_id = user_ids[random.randint(0, len(user_ids) - 1)]
        items = []
        for _ in range(random.randint(1, 5)):
            item_id = menu_items[random.randint(0, len(menu_items) - 1)][0]
            quantity = random.randint(1, 5)
            items.append({"item_id": item_id, "quantity": quantity})
        use_points = 0 if random.random() < 0.9 else random.randint(1, 10)
        response = requests.post(f"{BASE_URL}/transaction",
                                    json={
                                        "user_id": user_id,
                                        "group_id": user_groups[user_id][random.randint(0, len(user_groups[user_id]) - 1)],
                                        "items": items,
                                        "use_points": use_points
                                        })
        if response.status_code != 200:
            print(response.text, response.status_code)
            time.sleep(1)
            continue
        data = response.json()
        print(data)
        time.sleep(1)

def display_menu():
    menu = [
        ["1", "Signup group"],
        ["2", "Signup user"],
        ["3", "Login"],
        ["4", "Get Menu Items"],
        ["5", "Make Transaction"],
        ["6", "Get Transactions"],
        ["7", "Get Group"],
        ["8", "Get User"],
        ["9", "Join a Group"],
        ["10", "Run Scenario"],
        ["0", "Exit"]
    ]
    
    print("\nMenu:")
    print(tabulate(menu, headers=["Option", "Action"], tablefmt="rounded_outline", numalign="center"))
    print("Enter 'm' or 'M' to display menu again.\n")

def main():
    """
    Main function.
    """
    display_menu()
    while True:
        try:
            choice = input("> ")

            if choice == 'M' or choice == 'm':
                display_menu()
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
            elif choice == '9':
                join_group()
            elif choice == '10':
                run_scenario()
            elif choice == '0':
                break
        except KeyboardInterrupt:
            print()

if __name__ == "__main__":
    main()