import mysql.connector

try:
    connection = mysql.connector.connect(host="localhost", port="5432", 
                    database="global_cafe", user="postgres", password="postgres")
    crsr = connection.cursor()
    print("Connected to the database")

    #print("version: ")

    crsr.execute("""SELECT Users.user_id, Users.username, Users.email
    FROM Group_Members
    JOIN Users ON Group_Members.user_id = Users.user_id
    WHERE Group_Members.group_id = 2;
    """)

    version = crsr.fetchall()
    print(version)

    crsr.execute("""
INSERT INTO Group_Members (group_id, user_id)
VALUES (1, '3ccccc');

UPDATE User_Groups
SET number_members = number_members + 1
WHERE group_id = 1;
""")
    
    crsr.execute("""SELECT Users.user_id, Users.username, Users.email
    FROM Group_Members
    JOIN Users ON Group_Members.user_id = Users.user_id
    WHERE Group_Members.group_id = 1;
    """)

    version = crsr.fetchall()
    print(version)
except Exception as e:
    print("Error: ", e)