from fastapi import FastAPI
from .database import engine  # Importamos engine desde database.py
from . import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}