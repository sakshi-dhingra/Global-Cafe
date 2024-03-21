import psycopg2

connection = psycopg2.connect(host="localhost", port="5432", 
                    database="global_cafe", user="postgres", password="postgres")

crsr = connection.cursor()

print("version: ")

crsr.execute("""SELECT u.username, u.email, g.discount_points
FROM Users u
JOIN User_Groups g ON u.group_id = g.group_id
WHERE u.group_id = 1; """)

version = crsr.fetchall()
print(version)