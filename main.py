from datetime import date
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from pymongo import MongoClient

import pandas as pd

from dotenv import dotenv_values

from bson.json_util import dumps, loads

from util.utilidades import get_lunes_semana, get_rango_fechas


config = dotenv_values(".env")

app = FastAPI()

#*We make a single connection when loading the API
@app.on_event("startup")
async def startup_event():
    """
    Startup event.
    """
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]

#*We turn it off
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event.
    """
    app.mongodb_client.close()

#*It only accepts a date and a period of time between 
#* daily, weekly & monthly
class QueryData(BaseModel):
    date: date
    period: Literal['daily', 'weekly', 'monthly']

#*From here we begin to build the paths (rutas)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the KWH API"}

#*this is the most complex path
#*post type path (ruta de tipo post):
@app.post("/consumption")
async def compute(query: QueryData):
    """
    Compute consumption.

    :param query: Query data.
    """
#*depending on the value of query.period performs the query (consulta)
    if query.period == 'daily':

#*we convert date into a string since in mongodb the dates are in string        
        date = query.date.strftime('%Y-%m-%d')

#*enter the database, go to the data collection and search for the specified date and sort it from the oldest to the most recent date
        documents = app.database['data'].find({'meter_date': {'$regex': f'^{date}'}}, {'_id': 0}).sort('meter_date', 1)
        documents = loads(dumps(documents))

        return process_daily(documents) if len(documents) else []
    elif query.period == 'weekly':
        monday = get_lunes_semana(query.date)
        week = get_rango_fechas(monday)

        documents = []

        for day in week:
            date = day.strftime('%Y-%m-%d')

            result = app.database['data'].find({'meter_date': {'$regex': f'^{date}'}}, {'_id': 0}).sort('meter_date', 1)
            result = loads(dumps(result))

            if len(result):
                first = result[0]
                last = result[-1]

                documents.append({
                    'value': last['value'] - first['value'],
                    'meter_date': day.strftime('%Y-%m-%d %H:00:00')
                })
        
        return documents
    elif query.period == 'monthly':
        month = query.date.strftime('%Y-%m')
        result = app.database['data'].find({'meter_date': {'$regex': f'^{month}'}}, {'_id': 0}).sort('meter_date', 1)
        result = loads(dumps(result))

        return process_monthly(result) if len(result) else []
    else:
        return {"message": "Hello World else"}

#*The function receives a list of documents that was obtained from the database.
def process_daily(documents: list):
    """
    Process daily data.

    :param documents: List of documents.
    """
    #* Create dataframe:
    df = pd.DataFrame(documents)
    #*we convert meter_date to a date object (objeto fecha)
    #*cause it comes as a string
    df['meter_date'] = pd.to_datetime(df['meter_date'])
    #* we group it by hour
    groups = df.groupby(df['meter_date'].dt.hour)

    rows = []
    for _, group in groups:
        row = {}
    #*Para calcular cuanto se ha consumido las especificaciones de la prueba dicen:
    #*restele a la ultima medida (iloc.[-1]) a la primera que esta en la  posicion [0]
        row['value'] = group.iloc[-1]['value'] - group.iloc[0]['value']
    # y nos quedamos con la ultima hora, me da la fecha completa, la formateo
    # solo me interesa la hora asi que los min y seg los dejo en 0
        row['meter_date'] = group.iloc[-1]['meter_date'].strftime('%Y-%m-%d %H:00:00')
        rows.append(row)

    return rows


def process_monthly(result: list):
    """
    Process monthly data.

    :param result: List of documents.
    """
    # Create dataframe:
    df = pd.DataFrame(result)

    df['meter_date'] = pd.to_datetime(df['meter_date'])

    groups = df.groupby(df['meter_date'].dt.day)

    rows = []
    for _, group in groups:
        row = {}
        row['value'] = group.iloc[-1]['value'] - group.iloc[0]['value']
        row['meter_date'] = group.iloc[-1]['meter_date'].strftime('%Y-%m-%d 00:00:00')
        rows.append(row)

    return rows
