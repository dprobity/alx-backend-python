import sqlite3
import functools
from datetime import datetime

#### decorator to log SQ\l queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"[LOG] Executing SQL Query: {kwargs.get('query')}")
        return func(*args, **kwargs)
    return wrapper



@log_queries
def fetch_all_users(qwery):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(qwery)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query 
users = fetch_all_users(qwery="SELECT * FROM users")