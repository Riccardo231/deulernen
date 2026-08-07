import random
from database import connessione


modalita = "scheda"


def limite_tentativi():

    if modalita == "scheda":
        return 10
    else:
        return 2



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
        (p[0],0,0,"scheda")
        for p in parole
    ]


    cur.executemany("""
    INSERT INTO scheda_attiva
    (
        parola_id,
        de_it,
        it_de,
        tipo
    )
    VALUES (%s,%s,%s,%s)
    """, dati)


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
        (p[0],0,0,"ripasso")
        for p in parole
    ]


    cur.executemany("""
    INSERT INTO scheda_attiva
    (
        parola_id,
        de_it,
        it_de,
        tipo
    )
    VALUES (%s,%s,%s,%s)
    """, dati)


    conn.commit()

    cur.close()
    conn.close()






def ripasso_in_corso():

    conn = connessione()
    cur = conn.cursor()


    cur.execute("""
    SELECT COUNT(*)
    FROM scheda_attiva
    WHERE tipo='ripasso'
    AND
    (
        de_it < 2
        OR it_de < 2
    )
    """)


    n = cur.fetchone()[0]


    cur.close()
    conn.close()


    return n > 0







def scheda_in_corso():

    conn = connessione()
    cur = conn.cursor()


    cur.execute("""
    SELECT COUNT(*)
    FROM scheda_attiva
    WHERE tipo='scheda'
    AND
    (
        de_it < 10
        OR it_de < 10
    )
    """)


    n = cur.fetchone()[0]


    cur.close()
    conn.close()


    return n > 0








def prossima_parola():

    conn = connessione()
    cur = conn.cursor()


    limite = limite_tentativi()


    cur.execute("""
    SELECT

        s.parola_id,
        p.tedesco,
        p.italiano,
        s.de_it,
        s.it_de

    FROM scheda_attiva s

    JOIN parole p
    ON p.id=s.parola_id


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



    direzione=random.choice(direzioni)



    if direzione=="DE → IT":

        return {

            "parola_id":r[0],
            "domanda":r[1],
            "risposta":r[2],
            "direzione":direzione,
            "corrette":r[3]

        }



    return {

        "parola_id":r[0],
        "domanda":r[2],
        "risposta":r[1],
        "direzione":direzione,
        "corrette":r[4]

    }








def aggiorna_risposta(parola_id,direzione):

    conn = connessione()
    cur = conn.cursor()



    if direzione=="DE → IT":

        cur.execute("""
        UPDATE scheda_attiva

        SET de_it=de_it+1

        WHERE parola_id=%s
        """,
        (parola_id,))


    else:

        cur.execute("""
        UPDATE scheda_attiva

        SET it_de=it_de+1

        WHERE parola_id=%s
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


    fatti=cur.fetchone()[0]



    if modalita=="scheda":

        totale=4000


    else:

        cur.execute("""
        SELECT COUNT(*)
        FROM indici
        """)


        n=cur.fetchone()[0]


        totale=n*4



    cur.close()
    conn.close()


    return fatti,totale
