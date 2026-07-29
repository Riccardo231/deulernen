import random
from database import connessione


modalita = "scheda"


def crea_scheda():

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM scheda_attiva
    """)

    cur.execute("""
    SELECT id
    FROM parole
    WHERE id NOT IN
    (
        SELECT parola_id
        FROM indici
    )
    ORDER BY RANDOM()
    LIMIT 200
    """)

    parole = cur.fetchall()


    dati = [
        (p[0], 0, 0)
        for p in parole
    ]


    cur.executemany("""
    INSERT INTO scheda_attiva
    (
        parola_id,
        de_it,
        it_de
    )
    VALUES (%s,%s,%s)
    """,
    dati)


    conn.commit()

    cur.close()
    conn.close()



def crea_ripasso():

    conn = connessione()
    cur = conn.cursor()


    cur.execute("""
    DELETE FROM scheda_attiva
    """)


    cur.execute("""
    SELECT parola_id
    FROM indici
    """)


    parole = cur.fetchall()


    dati = [
        (p[0],0,0)
        for p in parole
    ]


    cur.executemany("""
    INSERT INTO scheda_attiva
    (
        parola_id,
        de_it,
        it_de
    )
    VALUES (%s,%s,%s)
    """,
    dati)


    conn.commit()

    cur.close()
    conn.close()





def prossima_parola():

    conn = connessione()
    cur = conn.cursor()


    limite = 10 if modalita == "scheda" else 2


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


    WHERE s.de_it < %s
       OR s.it_de < %s


    ORDER BY RANDOM()

    LIMIT 1

    """,
    (
        limite,
        limite
    ))


    r = cur.fetchone()


    cur.close()
    conn.close()


    if r is None:
        return None


    direzioni = []


    if r[3] < limite:
        direzioni.append("DE → IT")


    if r[4] < limite:
        direzioni.append("IT → DE")


    direzione = random.choice(direzioni)



    if direzione == "DE → IT":

        return {

            "parola_id": r[0],
            "domanda": r[1],
            "risposta": r[2],
            "direzione": direzione,
            "corrette": r[3]

        }


    else:

        return {

            "parola_id": r[0],
            "domanda": r[2],
            "risposta": r[1],
            "direzione": direzione,
            "corrette": r[4]

        }





def aggiorna_risposta(
        parola_id,
        direzione):


    conn = connessione()
    cur = conn.cursor()


    if direzione == "DE → IT":

        cur.execute("""
        UPDATE scheda_attiva

        SET de_it = de_it + 1

        WHERE parola_id = %s
        """,
        (parola_id,))


    else:

        cur.execute("""
        UPDATE scheda_attiva

        SET it_de = it_de + 1

        WHERE parola_id = %s
        """,
        (parola_id,))


    conn.commit()

    cur.close()
    conn.close()





def progresso():

    conn = connessione()
    cur = conn.cursor()


    cur.execute("""
    SELECT COALESCE(SUM(de_it+it_de),0)
    FROM scheda_attiva
    """)


    fatti = cur.fetchone()[0]


    if modalita == "scheda":

        totale = 200 * 10 * 2


    else:

        cur.execute("""
        SELECT COUNT(*)
        FROM indici
        """)

        n = cur.fetchone()[0]

        totale = n * 2 * 2


    cur.close()
    conn.close()


    return fatti, totale