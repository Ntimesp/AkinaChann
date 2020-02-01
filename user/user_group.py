import os
import sqlite3

def get_user_group_info(group_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    records = cursor.execute('SELECT * FROM user_group WHERE group_id=? ', (group_id, )).fetchall()
    
    lib.close()

    if not len(records):
        return 'unknown_user_group'
    
    return records[0]

def add_unknown_user_group(group_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    cursor.execute("INSERT INTO user_group VALUES (?, 'None', 1)", (group_id, ))

    lib.commit()
    lib.close()

def detect_user_group(group_id):
    record = get_user_group_info(group_id)
    if record == 'unknown_user_group':
        print('add_user_group: ', group_id)
        add_unknown_user_group(group_id)
    else:
        print(record)
