import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  cantidad INTEGER NOT NULL
)
''')


cursor.executemany("INSERT INTO productos (nombre, cantidad) VALUES (?,?)",
[
  ("Teclado", 10),
  ("Mouse", 25),
  ("Monitor",5),
])

conn.commit()
conn.close()