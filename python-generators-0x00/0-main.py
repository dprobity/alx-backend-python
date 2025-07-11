#!/usr/bin/python3

seed = __import__('seed')  # imports your seed.py functions

# Connect to MySQL (no DB yet)
connection = seed.connect_db()
if connection:
    # Create database
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    # Reconnect to new DB
    connection = seed.connect_to_prodev()

    if connection:
        # Create table
        seed.create_table(connection)

        # Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')

        # Test that the DB exists
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")

        # Show sample data
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
