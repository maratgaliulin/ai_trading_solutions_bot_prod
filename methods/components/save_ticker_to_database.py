import sqlite3

from methods.components.fetch_ticker_from_database import fetch_ticker

def save_ticker_to_database(table_name:str, ticker:str, purchase_price:float, purchase_amount:int, user_id:int, db_directory:str):
    f_ticker = fetch_ticker(table_name, ticker, user_id)
    message_success = "Данные успешно сохранены."
    message_is_modified = "Данные успешно изменены."
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    if (f_ticker is None):
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, ticker TEXT, user_id INTEGER, purchase_price REAL, purchase_amount INTEGER)''')
        cursor.execute(f"INSERT INTO {table_name} (ticker, purchase_price, purchase_amount, user_id) VALUES ('{ticker}', {purchase_price}, {purchase_amount}, {user_id})")
        conn.commit()
        conn.close()
        return message_success
    else:
        cursor.execute(f"UPDATE {table_name} SET purchase_price={purchase_price}, purchase_amount={purchase_amount}  WHERE user_id={user_id} AND ticker='{ticker}'")
        conn.commit()
        conn.close()
        return message_is_modified