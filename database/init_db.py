import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

cursor.execute(''' CREATE TABLE teach (question text, answer text, author text, env text) ''')

cursor.execute("INSERT INTO teach VALUES ('早上好', '你好呀，$s', '1553095676', 'global' )")
cursor.execute("INSERT INTO teach VALUES ('晚安', '晚安好梦，$s', '1553095676', 'global' )")
# cursor.execute("INSERT INTO teach VALUES ('test', 'test', 'unknown', 'global' ) ")

lib.commit()
lib.close()