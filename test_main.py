from fastapi.testclient import TestClient

from pymongo import MongoClient
from dotenv import dotenv_values

import pytest

config = dotenv_values(".env")

from main import app

app.mongodb_client = MongoClient(config['ATLAS_URI'])
app.database = app.mongodb_client[config['DB_NAME']]


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_compute_daily_non_exist(client):
    response = client.post("/consumption", json={"date": "2022-03-01", "period": "daily"})
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_compute_daily_exist(client):
    response = client.post("/consumption", json={"date": "2022-10-12", "period": "daily"})
    assert response.status_code == 200

    expected_records = 20

    assert len(response.json()) == expected_records


def test_compute_daily_exist_first_record(client):
    response = client.post("/consumption", json={"date": "2022-10-12", "period": "daily"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 20
    assert len(records) == expected_records

    expected_first_record = {
        "meter_date": "2022-10-12 02:00:00",
        "value": 3.1815199999999777
    }

    first_record = records[0]

    assert first_record['value'] == expected_first_record['value']
    assert first_record['meter_date'] == expected_first_record['meter_date']


def test_compute_daily_exist_last_record(client):
    response = client.post("/consumption", json={"date": "2022-10-12", "period": "daily"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 20
    assert len(records) == expected_records

    expected_last_record = {
        "meter_date": "2022-10-12 23:00:00",
        "value": 3.8347100000000864
    }

    last_record = records[-1]

    assert last_record['value'] == expected_last_record['value']
    assert last_record['meter_date'] == expected_last_record['meter_date']


def test_compute_weekly_exist_first_record(client):
    response = client.post("/consumption", json={"date": "2022-10-26", "period": "weekly"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 7
    assert len(records) == expected_records

    expected_first_record = {
        "meter_date": "2022-10-24 00:00:00",
        "value": 571.7084999999997
    }

    first_record = records[0]

    assert first_record['value'] == expected_first_record['value']
    assert first_record['meter_date'] == expected_first_record['meter_date']


def test_compute_weekly_exist_last_record(client):
    response = client.post("/consumption", json={"date": "2022-10-26", "period": "weekly"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 7
    assert len(records) == expected_records

    expected_last_record = {
        "meter_date": "2022-10-30 00:00:00",
        "value": 433.6816400000007
    }

    last_record = records[-1]

    assert last_record['value'] == expected_last_record['value']
    assert last_record['meter_date'] == expected_last_record['meter_date']


def test_compute_monthly_exist_first_record(client):
    response = client.post("/consumption", json={"date": "2022-10-26", "period": "monthly"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 20
    assert len(records) == expected_records

    expected_first_record = {
        "meter_date": "2022-10-12 00:00:00",
        "value": 539.75958
    }

    first_record = records[0]

    assert first_record['value'] == expected_first_record['value']
    assert first_record['meter_date'] == expected_first_record['meter_date']


def test_compute_monthly_exist_first_record(client):
    response = client.post("/consumption", json={"date": "2022-10-26", "period": "monthly"})
    assert response.status_code == 200
    
    records = response.json()
    expected_records = 20
    assert len(records) == expected_records

    expected_last_record = {
        "meter_date": "2022-10-31 00:00:00",
        "value": 305.53125
    }

    last_record = records[-1]

    assert last_record['value'] == expected_last_record['value']
    assert last_record['meter_date'] == expected_last_record['meter_date']
