from config import *
import sqlite3

from .fetch_ruble_position import fetch_ruble_position

def delete_ruble_position(user_id:int) -> str:
    message_success = "Рублевая позиция успешно удалена"
    message_failure = "Рублевая позиция не найдена"
    fetch_rub_pos = fetch_ruble_position(user_id)
    if (fetch_rub_pos is not None):
        conn = sqlite3.connect(db_directory)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM ruble_position WHERE client_id={user_id}")
        conn.commit()
        conn.close()
        return message_success
    else:
        return message_failure
