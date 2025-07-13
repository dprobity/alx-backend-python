from seed import connect_to_prodev

def stream_user_ages():
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age from user_data")
    for row in cursor:
        yield float(row['age'])
    conn.close()


def compute_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1
    return total/ count if count else 0
