import mysql.connector
import uuid
import csv




def connect_db():
    try:
        connection =  mysql.connector.connect(
            host="localhost",
            user="root",
            password="Qwertykey1!@"
        )

        return connection 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Qwertykey1!@",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")

        return None
    

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
                   user_id VARCHAR(36) PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   email VARCHAR(255) NOT NULL,
                   age DECIMAL NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                user_id = str(uuid.uuid4())  # generate a UUID
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))
            except mysql.connector.Error as err:
                print(f"Insert error: {err}")
    connection.commit()
    cursor.close()
    print("Data inserted successfully")