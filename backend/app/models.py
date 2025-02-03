from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sentencia(Base):
    __tablename__ = 'sentencia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rol = Column(String, nullable=False)
    caratulado = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    tribunal = Column(String, nullable=False)
    materia = Column(String, nullable=False)
    juez = Column(String, nullable=False)
    enlace = Column(String, nullable=False)

