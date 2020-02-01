import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

cursor.execute(''' CREATE TABLE user (user_id text, nickname text, authority integer) ''')

cursor.execute("INSERT INTO user VALUES ('1553095676', 'None', 5)")

lib.commit()
lib.close()