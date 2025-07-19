import sqlite3

class ExecuteQuery:

    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.qwery = query
        self.params = params or ()
        self.conn = None
        self.result = None


    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result 
    
    def __exit__(self, exec_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()



if __name__ == "__main__":
    qwery = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery("my_database.db", qwery, params) as results:
        for row in results:
            print(row)

