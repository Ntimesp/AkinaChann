import os
import sqlite3
from user.user_group import *
import time

def get_user_info(user_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    records = cursor.execute('SELECT * FROM user WHERE user_id=? ', (user_id, )).fetchall()
    
    lib.close()

    if not len(records):
        return 'unknown_user'
    
    return records[0]

def add_unknown_user(user_id, group_id, authority):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    cursor.execute("INSERT INTO user VALUES (?, 'None', ?)", (user_id, authority))

    lib.commit()
    lib.close()

def update_user_authority(user_id, authority):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    cursor.execute('UPDATE user SET authority=? WHERE user_id=?', (authority, user_id))
    
    lib.commit()
    lib.close()

def detect_user(user_id, group_id):
    default_authority = get_user_group_info(group_id)[2]

    record = get_user_info(user_id)
    if record == 'unknown_user':
        print('add_user: ', user_id)
        add_unknown_user(user_id, group_id, default_authority)
    else:
        if record[2] < default_authority:
            update_user_authority(user_id, default_authority)
        print(record)
    
    # cmd part
    record = get_user_cmd_info(user_id)
    print(record)
    if record == 'unknown_user':
        print('add user to cmd:{}'.format(user_id))
        add_to_user_cmd(user_id)

        


def get_user_cmd_info(user_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    records = cursor.execute('SELECT * FROM user_cmd WHERE user_id=? ', (user_id, )).fetchall()
    
    lib.close()

    if not len(records):
        return 'unknown_user'
    
    return records[0]

def add_to_user_cmd(user_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    cursor.execute("INSERT INTO user_cmd VALUES (?, ?)", (user_id, 4))

    lib.commit()
    lib.close()

def image_cmd_used(user_id):
    new_val = get_user_cmd_info(user_id)[1] - 1

    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    cursor.execute('UPDATE user_cmd SET image=? WHERE user_id=?', (new_val, user_id))
    
    lib.commit()
    lib.close()

def refresh_cmd():
    lib = sqlite3.connect(os.path.join('database', 'data.db'))
    cursor = lib.cursor()

    cursor.execute('UPDATE user_cmd SET image=?', (4,))

    lib.commit()
    lib.close()

def checkdate():
    f = open('date.txt', 'r')
    old_time = f.read()
    f.close()
    cur_time = time.strftime("%Y-%m-%d", time.localtime()) 
    if cur_time != old_time:
        f = open('date.txt', 'w')
        f.write(cur_time)
        f.close()
        refresh_cmd()
    