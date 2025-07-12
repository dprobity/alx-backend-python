from seed import connect_to_prodev

def stream_users():
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)  # rows as dicts
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # í´¥ this is the generator magic

    cursor.close()
    connection.close()

