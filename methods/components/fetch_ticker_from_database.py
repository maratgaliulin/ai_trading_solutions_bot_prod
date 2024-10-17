from config import *
import sqlite3

def fetch_ticker(table_name:str, ticker:str, user_id:int):
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE user_id = {user_id} AND ticker = '{ticker}'")
    result = cursor.fetchone()
    conn.close()
    return result