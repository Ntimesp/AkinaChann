import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

records = cursor.execute('SELECT * FROM user').fetchall()

cursor.execute(''' CREATE TABLE user_cmd (user_id text, image integer) ''')

lib.commit()
lib.close()
