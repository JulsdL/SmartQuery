import sqlite3

def initialize_database():
    conn = sqlite3.connect('database/Chinook.db')
    cursor = conn.cursor()
    with open('database/Chinook_Sqlite.sql', 'r') as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
