import sqlite3
from methods.components.fetch_ruble_position import fetch_ruble_position

def save_ruble_position(user_id:int, ruble_position:float, db_directory:str):
    message_success = "Рублевая позиция сохранена."
    message_position_modified = "Рублёвая позиция модифицирована."

    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    if (fetch_ruble_position(user_id) is None):
        cursor.execute(f"INSERT INTO ruble_position (client_id, ruble_position) VALUES ({user_id}, {ruble_position})")
        conn.commit()
        conn.close()
        return message_success
    else:
        cursor.execute(f"UPDATE ruble_position SET ruble_position={ruble_position} WHERE client_id={user_id}")
        conn.commit()
        conn.close()
        return message_position_modified

    