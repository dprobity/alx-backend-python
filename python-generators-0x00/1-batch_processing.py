import mysql.connector


def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Qwertykey1!@",
        database="ALX_prodev"
            
    )



def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()

    if not connection:
        return
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * from user_data")

    while True:
        batch = cursor.fetchmany(size=batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user["age"]) > 25:
                print(user)


















# from seed import connect_to_prodev

# def stream_users_in_batches(batch_size):
#     connection = connect_to_prodev()
#     if not connection:
#         return
    

#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM  user_data")

#     while True:
#         batch  = cursor.fetchmany(size=batch_size)
#         if not batch:
#             break
#         yield batch 

#     cursor.close()
#     connection.close()




# def batch_processing(batch_size):
#     for batch in stream_users_in_batches(batch_size):
#         for user in batch:
#             if float(user["age"]) > 25:    # Cast to float in case age is Decimal
#                 print(user)