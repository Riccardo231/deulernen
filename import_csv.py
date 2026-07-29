import sqlite3

VECCHIO_DB = "../dlf/flashcards.db"

sqlite = sqlite3.connect(VECCHIO_DB)
cursor = sqlite.cursor()

cursor.execute("""
SELECT name 
FROM sqlite_master
WHERE type='table';
""")

print(cursor.fetchall())

sqlite.close()