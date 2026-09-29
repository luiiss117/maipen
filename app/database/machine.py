import sqlite3
from app.database import db_name

database = db_name
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

def get_machine_by_userid(user_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id, name, ip_address, operating_system, created_at, uid, description FROM machines WHERE user_id =? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            row = cur.fetchall()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print('Error:', e)

def get_machine_by_userid_and_uuid(user_id, machine_uuid):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id,name,ip_address,operating_system,description,created_at,uid FROM machines WHERE user_id =? AND uid=? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,machine_uuid))
            row = cur.fetchone()
            if row:
                return row
            else:
                return None
    except sqlite3.OperationalError as e:
        print("Error", e)

def get_machineid_by_userid_and_uuid(user_id, machine_uuid):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' SELECT id FROM machines WHERE user_id =? AND uid=? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,machine_uuid))
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                return None
    except sqlite3.OperationalError as e:
        print("Error", e)

def delete_machine(user_id, machine_uuid):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' DELETE FROM machines WHERE user_id =? AND uid=? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,machine_uuid))
    except sqlite3.OperationalError as e:
        print("Error", e)

def delete_all_machines_by_userid(user_id):
    try:
        with sqlite3.connect(database) as conn:
            sql = ''' DELETE FROM machines WHERE user_id =? '''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
    except sqlite3.OperationalError as e:
        print("Error", e)

