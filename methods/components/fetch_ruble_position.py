from config import *
import sqlite3

def fetch_ruble_position(user_id:int) -> float:
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    cursor.execute(f"SELECT ruble_position FROM ruble_position WHERE client_id = {user_id}")
    result = cursor.fetchone()
    conn.close()
    return result