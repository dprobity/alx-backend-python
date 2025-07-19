import sqlite3



class Databaseconnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn= None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn
    
    def __exit__(self, exec_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()



if __name__ == "__main__":
    with Databaseconnection("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)