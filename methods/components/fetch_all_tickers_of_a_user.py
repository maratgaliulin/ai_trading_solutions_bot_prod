from config import *
import sqlite3

def fetch_all_tickers_of_a_user(table_name:str, user_id:int, db_directory:str):
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    cursor.execute(f"SELECT ticker, purchase_price, purchase_amount FROM {table_name} WHERE user_id = {user_id}")
    result = cursor.fetchall()
    conn.close()
    return result