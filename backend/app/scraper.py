import requests
from bs4 import BeautifulSoup
from .database import SessionLocal
from .models import Sentencia

def fetch_data():
    url = "https://juris.pjud.cl/busqueda?Sentencias_Penales"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    sentences_data = []
    results = soup.find_all("div", class_="card border-info")

    for result in results:
        sentencia = {}
        
                # Buscar "ROL"
        rol = result.find("span", text=lambda text: text and text.startswith("ROL:"))
        if rol:
            rol_text = rol.text.split("ROL:")[-1].strip()
            sentencia["rol"] = rol_text
        else:
            sentencia["rol"] = None
        print(f"ROL: {sentencia['rol']}")  # Log para depuración

        caratulado = result.find("span", string=lambda text: text and text.startswith("Caratulado:"))
        if caratulado:
            sentencia["caratulado"] = caratulado.text.split("Caratulado:")[-1].strip()
        else:
            sentencia["caratulado"] = None
        print(f"Caratulado: {sentencia['caratulado']}")  # Log para depuración

        fecha = result.find("span", string=lambda text: text and text.startswith("Fecha:"))
        if fecha:
            sentencia["fecha"] = fecha.text.split("Fecha:")[-1].strip()
        else:
            sentencia["fecha"] = None
        print(f"Fecha: {sentencia['fecha']}")  # Log para depuración

        tribunal = result.find("span", text=lambda text: text and text.startswith("Tribunal:"))
        if tribunal:
            tribunal_text = tribunal.text.split("Tribunal:")[-1].strip()
            sentencia["tribunal"] = tribunal_text
        else:
            sentencia["tribunal"] = None
        print(f"Tribunal: {sentencia['tribunal']}")  # Log para depuración

        materia = result.find("span", string=lambda text: text and text.startswith("Materia:"))
        if materia:
            sentencia["materia"] = materia.text.split("Materia:")[-1].strip()
        else:
            sentencia["materia"] = None
        print(f"Materia: {sentencia['materia']}")  # Log para depuración

        juez = result.find("span", string=lambda text: text and text.startswith("Juez(a):"))
        if juez:
            sentencia["juez"] = juez.text.split("Juez(a):")[-1].strip()
        else:
            sentencia["juez"] = None
        print(f"Juez(a): {sentencia['juez']}")  # Log para depuración

        enlace = result.find("a", {"id": "url_enlace_sentencia_panel_resultados_0"})
        if enlace:
            sentencia["enlace"] = enlace["href"]
        else:
            sentencia["enlace"] = None
        print(f"Enlace: {sentencia['enlace']}")  # Log para depuración

        sentences_data.append(sentencia)

    return sentences_data

def save_sentences_to_db(sentences_data):
    db = SessionLocal()
    for data in sentences_data:
        if data.get("rol") is not None:  # Solo guardamos si el 'rol' no es None
            db.add(Sentencia(**data))
    db.commit()
    db.close()

async def scrape_and_save_data():
    sentences_data = fetch_data()
    save_sentences_to_db(sentences_data)
