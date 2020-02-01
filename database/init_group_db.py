import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

cursor.execute(''' CREATE TABLE user_group (group_id text, alias text, authority integer) ''')

cursor.execute("INSERT INTO user_group VALUES ('250253824', 'nsfz_acg', 2)")

lib.commit()
lib.close()