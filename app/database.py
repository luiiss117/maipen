import sqlite3

database = "maipen.db"
def init_db():
    try:
        with sqlite3.connect(database) as conn:
            print(f'Created/opened database with version {sqlite3.sqlite_version} successfully.')
            # create a cursor
            cursor = conn.cursor()
            sql_tables_statements = [
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
            );""",

            """CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            operating_system TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            uid TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
            );""",

            """CREATE TABLE IF NOT EXISTS machine_services (
            id INTEGER PRIMARY KEY,
            port INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            protocol TEXT NOT NULL,
            version TEXT NOT NULL,
            state TEXT NOT NULL,
            machine_id INTEGER NOT NULL,
            FOREIGN KEY(machine_id) REFERENCES machines(id)
            );""",

            """CREATE TABLE IF NOT EXISTS machine_credentials (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            service TEXT NOT NULL,
            description TEXT NOT NULL,
            machine_id INTEGER NOT NULL,
            FOREIGN KEY(machine_id) REFERENCES machines(id)
            );""",

            """CREATE TABLE IF NOT EXISTS nmap_scans (
            id INTEGER PRIMARY KEY,
            output TEXT NOT NULL,
            machine_id INTEGER NOT NULL,
            FOREIGN KEY(machine_id) REFERENCES machines(id)
            );"""
            ]
            # execute statements to create the users and machines tables
            for statement in sql_tables_statements:
                cursor.execute(statement)

            # commit the changes
            conn.commit()
            print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print('An error happened:', e)

def add_new_user(user, password):
    try:
        with sqlite3.connect(database) as conn:
            # Insert table statement
            sql = ''' INSERT INTO users(username,password) VALUES(?,?) '''
            # Create a cursor
            cur = conn.cursor()
            # Execute the INSERT statement
            creds = (user, password)
            cur.execute(sql, creds)
            # commit the changes
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


def check_machine(user_id,machine_name):
    try:
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            sql_statement = ''' SELECT id FROM machines WHERE user_id =? AND name =?'''
            cur.execute(sql_statement, (user_id,machine_name))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.Error as e:
        print(e)

def add_new_machine(user_id,machine_name,machine_ip,machine_os,machine_description,creation_date,update_date,machine_uid):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' INSERT INTO machines(user_id,name,ip_address,operating_system,description,created_at,updated_at,uid) VALUES(?,?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,machine_name,machine_ip,machine_os,machine_description,creation_date,update_date,machine_uid))
            conn.commit()
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_machine(user_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id,name,ip_address,operating_system,created_at,uid FROM machines WHERE user_id =? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            row = cur.fetchall()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_machine_by_ids(user_id, machine_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id,name,ip_address,operating_system,created_at,uid FROM machines WHERE user_id =? AND uid=? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,uuid))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_machine_id(user_id,name):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id FROM machines WHERE name =? AND user_id =? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print('Error:', e)

