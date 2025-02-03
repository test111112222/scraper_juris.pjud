from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "postgresql://user:password@db/jurispjud"  # Cambia esto por tu URL de conexión

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Crear las tablas en la base de datos
    Base.metadata.create_all(bind=engine)
