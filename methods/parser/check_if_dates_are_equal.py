from datetime import datetime
import sqlite3
from config import *

def check_if_dates_are_equal() -> bool:
    dt_format = '%Y-%m-%d'
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    created_at = cursor.execute(f'SELECT created_at FROM rbc_news WHERE id=0').fetchone()[0]
    conn.commit()
    today_s_date = datetime.now().strftime(format=dt_format)
    print(created_at, today_s_date)
    conn.close()
    return created_at == today_s_date