# Solución de Prueba Técnica

## 1. Descripción

Este proyecto es una solución a la prueba técnica para rol como desarrollador backend.

## 2. Requerimientos

- Python 3.8 o superior
- MongoDB
- FastAPI
- Pytest

Los demás requerimientos se encuentran en el archivo `requirements.txt`

## 3. Instalación

### 3.1 Clonar el repositorio

`git clone https://github.com/anddregon/kwh.git`


### 3.2 Crear un entorno virtual

Ejecutar el siguiente sobre la carpeta donde se clonó el repositorio:

`python -m venv venv`

### 3.3 Activar el entorno virtual

`source venv/bin/activate` (Linux)

`venv\Scripts\activate` (Windows)

### 3.4 Instalar los requerimientos

`pip install -r requirements.txt`

### 3.5 Inicializar la base de datos

Es necesario crear un cluster de base de datos en MongoDB Atlas.

La base de datos debe llamarse `kwh` y la colección `data`.

Luego, se debe crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

`ATLAS_URI=<URI de conexión a la base de datos con las credenciales embebidas>`
`DB_NAME=kwh`

Luego ir a la carpeta `ini` y ejecutar el script `database.py`

### 3.6 Ejecutar el proyecto

`uvicorn main:app --reload`

## 4. Ejecutar los tests

`pytest`

Este comando se debe ejecutar en la carpeta raíz del proyecto.

## 5. Documentación

La documentación de la API se encuentra en la ruta `/docs` de la aplicación.

http://127.0.0.1:8000/docs

Vamos a `Consumption` y luego a `try it out` para probar
con diferentes fechas y si queremos que sea diario, semanal o mensual.
Luego damos click en `execute`.

## 6. Ejemplos

### 6.1 Prueba con curl para `daily`

`curl -X 'POST' \
  'http://localhost:8000/consumption' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2022-10-25",
  "period": "daily"
}'`


### 6.2 Prueba con curl para `weekly`

`
curl -X 'POST' \
  'http://localhost:8000/consumption' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2022-10-26",
  "period": "weekly"
}'
`

### 6.3 Prueba con curl para `monthly`

`
curl -X 'POST' \
  'http://localhost:8000/consumption' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2022-10-26",
  "period": "monthly"
}'
`
