import sqlite3
from psycopg2.extras import execute_values
from database import connessione

SQLITE_DB = "/Users/riccardoorsi/Desktop/dlf/flashcards.db"

# Legge SQLite
sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute("""
SELECT id, tedesco, italiano, genere
FROM parole
ORDER BY id
""")

parole = sqlite_cursor.fetchall()

sqlite_cursor.execute("""
SELECT DISTINCT valore
FROM indici
ORDER BY valore
""")

indici = sqlite_cursor.fetchall()

sqlite_conn.close()

print(f"Parole: {len(parole)}")
print(f"Indici: {len(indici)}")

# Scrive su PostgreSQL
pg_conn = connessione()
pg_cursor = pg_conn.cursor()

# Pulisce le tabelle
pg_cursor.execute("TRUNCATE TABLE indici, scheda_attiva, parole RESTART IDENTITY CASCADE")

# Inserisce parole
execute_values(
    pg_cursor,
    """
    INSERT INTO parole
    (id, tedesco, italiano, genere)
    VALUES %s
    """,
    parole
)

# Inserisce indici
execute_values(
    pg_cursor,
    """
    INSERT INTO indici
    (parola_id)
    VALUES %s
    """,
    indici
)

pg_conn.commit()

pg_cursor.close()
pg_conn.close()

print("Migrazione completata.")