import sqlite3

conn = sqlite3.connect('qwerty123.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
   user_name TEXT NOT NULL,
   attempst INTEGER DEFAULT 0, 
   salt TEXT,
   key_HMAC TEXT,
   public_key_RSA TEXT,
   private_key_RSA TEXT,
   key_AES TEXT);
""")



conn.commit()

def check_user_exist(username):
    cur.execute("SELECT user_name FROM users WHERE user_name == ?", [username])
    return True if cur.fetchone() is not None else False

def create_user(username, salt, key_HMAC, public_key_RSA, encrypted_key_RSA, encrypted_key_AES):
    #cur.execute("INSERT INTO users(user_name, key_HMAC) VALUES(?, ?);", (username, public_key_RSA))
    cur.execute("INSERT INTO users(user_name, salt, key_HMAC, public_key_RSA, private_key_RSA, key_AES) VALUES(?, ?, ?, ?, ?, ?);", (username, salt, key_HMAC, public_key_RSA, encrypted_key_RSA, encrypted_key_AES))
    create_user_db(username)
    conn.commit()

def create_user_db(username):
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("""CREATE TABLE IF NOT EXISTS pwds (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       address TEXT NOT NULL,
       login  TEXT NOT NULL, 
       password TEXT NOT NULL,
       comment TEXT);
    """)

def get_key(username):
    cur.execute("SELECT salt, public_key_RSA, private_key_RSA FROM users WHERE user_name == ?", [username])
    salt, public_key_RSA, encrypted_key_RSA = cur.fetchone()
    return salt, public_key_RSA, encrypted_key_RSA

def get_attempts(username):
    cur.execute("SELECT attempts FROM users WHERE user_name == ?", [username])
    attempts = cur.fetchone()
    return attempts

def set_attempts(username, val):
    if val <= 0: cur.execute("UPDATE users SET attempts = 0 WHERE user_name == ?", [username])
    elif val > 0: cur.execute("UPDATE users SET attempts = attempts+? WHERE user_name == ?", [val, username])
    conn.commit()

def add_element(username, address, login, password, comment=''):
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("INSERT INTO pwds(address, login, password, comment) VALUES(?, ?, ?, ?);", (address, login, password, comment))
    id = cur_db.lastrowid
    conn_db.commit()
    return id

def get_elements(username):
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("SELECT id, address, login, comment FROM pwds")
    res = cur_db.fetchmany(255)
    return res

def get_element(username, id):
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("SELECT * FROM pwds WHERE id==?", [id])
    res = cur_db.fetchone()
    return res


def get_AES(username):
    cur.execute("SELECT key_AES FROM users WHERE user_name == ?", [username])
    key_AES = cur.fetchone()
    return key_AES[0]


def delete_element(username, id):
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("DELETE FROM pwds WHERE id=?;", [id])
    conn_db.commit()


def edit_element(username, id, address, login, password, comment=''):
    print(type(id))
    conn_db = sqlite3.connect(f'{username}.db')
    cur_db = conn_db.cursor()
    cur_db.execute("""UPDATE pwds SET address = ?,
                    login=?,
                    password=?,
                    comment=?
                    WHERE id == ?;"""
                   ,(address, login, password, comment, id))
    id = cur_db.lastrowid
    conn_db.commit()
    return id



