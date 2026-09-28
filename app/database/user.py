import sqlite3
from app.database import db_name

database = db_name
def add_new_user(user, password):
    try:
        with sqlite3.connect(database) as conn:
            # Insert table statement
            sql = ''' INSERT INTO users(username,password) VALUES(?,?) '''
            cur = conn.cursor()
            creds = (user, password)
            cur.execute(sql, creds)
            conn.commit()
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_user_by_id(user_id):
    try:
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            sql_statement = "SELECT id,username,password FROM users WHERE id =?"
            cur.execute(sql_statement, (user_id,))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.Error as e:
        print(e)

def get_user_by_username(username):
    try:
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            sql_statement = "SELECT id,username,password FROM users WHERE username =?"
            cur.execute(sql_statement, (username,))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.Error as e:
        print(e)

def delete_account(user_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' DELETE FROM users WHERE id =? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
    except sqlite3.OperationalError as e:
        print("Error", e)

