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


@app.on_event("startup")
async def startup_event():
    """
    Startup event.
    """
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event.
    """
    app.mongodb_client.close()


class QueryData(BaseModel):
    date: date
    period: Literal['daily', 'weekly', 'monthly']


@app.get("/")
async def read_root():
    return {"message": "Welcome to the KWH API"}


@app.post("/consumption")
async def compute(query: QueryData):
    """
    Compute consumption.

    :param query: Query data.
    """
    if query.period == 'daily':
        date = query.date.strftime('%Y-%m-%d')

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


def process_daily(documents: list):
    """
    Process daily data.

    :param documents: List of documents.
    """
    # Create dataframe:
    df = pd.DataFrame(documents)

    df['meter_date'] = pd.to_datetime(df['meter_date'])
    
    groups = df.groupby(df['meter_date'].dt.hour)

    rows = []
    for _, group in groups:
        row = {}
        row['value'] = group.iloc[-1]['value'] - group.iloc[0]['value']
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
