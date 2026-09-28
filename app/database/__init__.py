import sqlite3

db_name = "maipen.db"
def init_db():
    try:
        with sqlite3.connect(db_name) as conn:
            print(f'Created/opened database with version {sqlite3.sqlite_version} successfully.')
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
            protocol TEXT NOT NULL,
            port INTEGER NOT NULL,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
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
            for statement in sql_tables_statements:
                cursor.execute(statement)

            conn.commit()
            print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print('An error happened:', e)


