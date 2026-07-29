import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
#postgresql://postgres.txtcovnmyozkcbrrejra:QpZKcFjtmxu3hmXH@aws-0-eu-west-3.pooler.supabase.com:5432/postgres

def connessione():
    return psycopg2.connect(DATABASE_URL)



# =========================
# PAROLE
# =========================

def carica_parole():

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, tedesco, italiano, genere
    FROM parole
    ORDER BY id
    """)

    risultato = cur.fetchall()

    cur.close()
    conn.close()

    return risultato



# =========================
# INDICI
# parole già completate
# =========================

def carica_indici():

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    SELECT parola_id
    FROM indici
    """)

    risultato = [
        riga[0]
        for riga in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return risultato



def salva_indice(parola_id):

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO indici
    (parola_id)
    VALUES (%s)
    ON CONFLICT (parola_id)
    DO NOTHING
    """,
    (parola_id,))

    conn.commit()

    cur.close()
    conn.close()



# =========================
# SCHEDA ATTIVA
# =========================

def svuota_scheda():

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM scheda_attiva
    """)

    conn.commit()

    cur.close()
    conn.close()



def aggiungi_parola_scheda(parola_id):

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO scheda_attiva
    (parola_id, de_it, it_de)
    VALUES (%s,0,0)
    """,
    (parola_id,))

    conn.commit()

    cur.close()
    conn.close()



def carica_scheda():

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        s.parola_id,
        p.tedesco,
        p.italiano,
        s.de_it,
        s.it_de
    FROM scheda_attiva s
    JOIN parole p
    ON p.id = s.parola_id
    """)

    risultato = cur.fetchall()

    cur.close()
    conn.close()

    return risultato



def aggiorna_progresso(parola_id, direzione):

    conn = connessione()
    cur = conn.cursor()


    if direzione == "DE_IT":

        cur.execute("""
        UPDATE scheda_attiva
        SET de_it = de_it + 1
        WHERE parola_id = %s
        """,
        (parola_id,))


    elif direzione == "IT_DE":

        cur.execute("""
        UPDATE scheda_attiva
        SET it_de = it_de + 1
        WHERE parola_id = %s
        """,
        (parola_id,))


    conn.commit()

    cur.close()
    conn.close()