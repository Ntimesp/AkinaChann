import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

records = cursor.execute('SELECT * FROM user').fetchall()


print(len(records))
for row in records:
    print(row)

lib.commit()
lib.close()