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
            description TEXT NOT NULL,
            created_at DATE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
            );""",

            """CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY,
            port INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            protocol TEXT NOT NULL,
            version TEXT NOT NULL,
            state TEXT NOT NULL,
            machine_id INTEGER NOT NULL,
            FOREIGN KEY(machine_id) REFERENCES machines(id)
            );""",

            """CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            username INTEGER NOT NULL,
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

def is_username_taken(check_user: str):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username =?", (check_user,))
        row = cur.fetchone()
        if row:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)

def check_user(username):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sql_statements = "SELECT role FROM users WHERE role = 'user' AND username = ?"
        cur.execute(sql_statements, (username,))
        row = cur.fetchone()
        if row:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)

def check_passw(username):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sql_statements = "SELECT password FROM users WHERE role = 'user' AND username = ?"
        cur.execute(sql_statements, (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return False

    except sqlite3.Error as e:
        print(e)

