import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

# cursor.execute('DELETE FROM teach where rowid=3')


records = cursor.execute('SELECT * FROM teach').fetchall()

print(len(records))
for row in records:
    print(row)

lib.commit()
lib.close()