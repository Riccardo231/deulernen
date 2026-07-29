from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import scheda


app = FastAPI()


templates = Jinja2Templates(
    directory="templates"
)


parola_corrente = None
errore = None



@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "menu": True
        }
    )





# CONTINUA LA SCHEDA ESISTENTE

@app.post("/scheda")
def avvia_scheda():

    global parola_corrente

    scheda.modalita = "scheda"

    parola_corrente = None


    return RedirectResponse(
        "/gioco",
        status_code=303
    )





# CREA UNA NUOVA SCHEDA DA ZERO

@app.post("/nuova_scheda")
def nuova_scheda():

    global parola_corrente

    scheda.modalita = "scheda"

    scheda.crea_scheda()

    parola_corrente = None


    return RedirectResponse(
        "/gioco",
        status_code=303
    )





# CREA RIPASSO

@app.post("/ripasso")
def avvia_ripasso():

    global parola_corrente

    scheda.modalita = "ripasso"

    scheda.crea_ripasso()

    parola_corrente = None


    return RedirectResponse(
        "/gioco",
        status_code=303
    )






@app.get("/gioco")
def gioco(request: Request):

    global parola_corrente


    if parola_corrente is None:

        parola_corrente = scheda.prossima_parola()



    fatti, totale = scheda.progresso()



    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={

            "domanda": parola_corrente,

            "errore": errore,

            "fatti": fatti,

            "totale": totale

        }
    )






@app.post("/risposta")
def risposta(
        risposta: str = Form(...)
):

    global parola_corrente
    global errore



    if risposta.strip().lower() == parola_corrente["risposta"].lower():


        scheda.aggiorna_risposta(
            parola_corrente["parola_id"],
            parola_corrente["direzione"]
        )


        parola_corrente = None
        errore = None


    else:

        errore = parola_corrente["risposta"]



    return RedirectResponse(
        "/gioco",
        status_code=303
    )







@app.post("/continua")
def continua():

    global parola_corrente
    global errore


    parola_corrente = None
    errore = None


    return RedirectResponse(
        "/gioco",
        status_code=303
    )
