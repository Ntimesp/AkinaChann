import os
import sqlite3

lib = sqlite3.connect(os.path.join('database', 'data.db'))

cursor = lib.cursor()

cursor.execute('UPDATE teach SET env=? WHERE env=?', ('global', 'globals'))

lib.commit()
lib.close()