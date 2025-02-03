from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, scraper, database
from .scraper import scrape_and_save_data

# Inicia la base de datos
database.init_db()

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/scrape")
async def scrape():
    await scrape_and_save_data()
    return {"message": "Data scraped and saved successfully"}