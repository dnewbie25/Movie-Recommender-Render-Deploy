# from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import functions

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes: str):
    return {'message': f'{functions.cantidad_filmaciones_mes(mes)} cantidad de peliculas que fueron estrenadas el mes de {mes.title()}'}
    # return templates.TemplateResponse("mes.html", {"request": request, "response_data": response_data})

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    return {'message':f"{functions.cantidad_filmaciones_dia(dia)} cantidad de peliculas que fueron estrenadas los dias {dia.title()}"}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo):
    return functions.score_titulo(titulo)

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo):
    return functions.total_votos(titulo)

@app.get('/get_actor/{actor}')
def get_actor(actor=''):
    return functions.get_actor(actor)

@app.get('/get_director/{director}')
def get_director(director=''):
    return functions.get_director(director)


# --->> the ML model is using more than the allocated RAM, need to optimize

@app.get('/movie_recommender/{titulo}')
def movie_recommender(titulo=''):
    return functions.recommend_movie(titulo)
