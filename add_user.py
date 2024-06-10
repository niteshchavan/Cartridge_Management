# To add users run "python add_user.py" 

import mysql.connector
import bcrypt

# Configure the MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="cartridges"
)

def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    db.commit()
    cursor.close()

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)
    print(f"User {username} added successfully.")
