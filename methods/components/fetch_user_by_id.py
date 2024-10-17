from config import *
import sqlite3

def fetch_user_by_id(userId):
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE telegram_id = {userId}')
    result = cursor.fetchone()
    conn.close()
    return result