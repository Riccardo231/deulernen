from fastapi import FastAPI
from pydantic import BaseModel

from scheda import prossima_parola, aggiorna


app = FastAPI()



@app.get("/")
def home():

    return {
        "messaggio":
        "Server flashcards attivo"
    }



@app.get("/scheda")
def scheda():

    parola = prossima_parola()

    return parola



class Risposta(BaseModel):

    parola_id:int
    direzione:str
    corretta:bool



@app.post("/risposta")
def risposta(r:Risposta):

    aggiorna(
        r.parola_id,
        r.direzione,
        r.corretta
    )

    return {
        "ok":True
    }