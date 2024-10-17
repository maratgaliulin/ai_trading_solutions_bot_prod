import sqlite3

# project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) 
# sys.path.append(project_directory)

class User:
    def __init__(self, telegram_id, username, telegram_nickname, db_directory):
        self.telegram_id = telegram_id
        self.db_directory = db_directory
        self.username = username
        self.telegram_nickname = telegram_nickname

    def write_data(self):
        conn = sqlite3.connect(self.db_directory)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, username TEXT, telegram_nickname TEXT)''')
        cursor.execute(f"INSERT INTO users VALUES ({self.telegram_id}, '{self.username}', '{self.telegram_nickname}')")
        # inserted_id = cursor.lastrowid
        conn.commit()
        conn.close()
        # return inserted_id
    
    def read_data(self):
        conn = sqlite3.connect(self.db_directory)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM users WHERE telegram_id = {self.telegram_id}')
        result = cursor.fetchone()
        conn.close()
        return result
