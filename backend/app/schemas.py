from pydantic import BaseModel
from datetime import datetime

class SentenciaBase(BaseModel):
    rol: str
    caratulado: str
    fecha: datetime
    tribunal: str
    materia: str
    juez_a: str
    enlace_sentencia: str

class SentenciaCreate(SentenciaBase):
    pass

class Sentencia(SentenciaBase):
    id: int

    class Config:
        orm_mode = True
