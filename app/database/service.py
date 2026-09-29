import sqlite3
from app.database import db_name

database = db_name

def add_new_service(protocol,port,name,version,machine_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' INSERT INTO machine_services(protocol,port,name,version,machine_id) VALUES(?,?,?,?,?)'''
            cur = conn.cursor()
            cur.execute(sql, (protocol,port,name,version,machine_id))
            conn.commit()
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_service_id(machine_id,port):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id FROM machine_services WHERE machine_id=? AND port=?'''
            cur = conn.cursor()
            cur.execute(sql, (machine_id,port))
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                return None
    except sqlite3.OperationalError as e:
        print("Error", e)


def get_service_port(machine_id,port):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT port FROM machine_services WHERE machine_id=? AND port=?'''
            cur = conn.cursor()
            cur.execute(sql, (machine_id,port))
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                return None
    except sqlite3.OperationalError as e:
        print("Error", e)

def get_all_services(machine_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT protocol,port,name,version FROM machine_services WHERE machine_id=?'''
            cur = conn.cursor()
            cur.execute(sql, (machine_id,))
            row = cur.fetchall()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print("Error", e)

def delete_service(machine_id, port):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' DELETE FROM machine_services WHERE machine_id =? AND port=? '''
            cur = conn.cursor()
            cur.execute(sql, (machine_id,port))

            conn.commit()
    except sqlite3.OperationalError as e:
        print("Error", e)

def delete_all_services(machine_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' DELETE FROM machine_services WHERE machine_id =?'''
            cur = conn.cursor()
            cur.execute(sql, (machine_id,))
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Error", e)
