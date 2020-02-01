import os 
import sqlite3
import random
from utils.string_utils import *
def answer(string, sender_name, group_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))

    cursor = lib.cursor()

    records = cursor.execute('SELECT answer FROM teach WHERE question=? AND (env=? OR env=?)', (string, group_id, 'global')).fetchall()
    records = [str_convert_esc(record[0]) for record in records]

    if (len(records)):
        choice = random.randint(0, len(records) - 1)

        lib.close()

        reply = records[choice]
        reply = reply.replace('$s', sender_name)

        return reply

    return False

    lib.close()
