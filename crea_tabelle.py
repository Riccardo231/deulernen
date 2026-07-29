from database import connessione

#export DATABASE_URL="postgresql://postgres.txtcovnmyozkcbrrejra:QpZKcFjtmxu3hmXH@aws-0-eu-west-3.pooler.supabase.com:5432/postgres"
conn = connessione()
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS parole (
    id SERIAL PRIMARY KEY,
    tedesco TEXT NOT NULL,
    italiano TEXT NOT NULL,
    genere TEXT
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS indici (
    parola_id INTEGER PRIMARY KEY REFERENCES parole(id)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS scheda_attiva (
    parola_id INTEGER PRIMARY KEY REFERENCES parole(id),
    de_it INTEGER DEFAULT 0,
    it_de INTEGER DEFAULT 0
);
""")


conn.commit()
conn.close()

print("Tabelle create")