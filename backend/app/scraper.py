from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import timedelta, datetime
from .database import SessionLocal
from .models import Sentencia

def fetch_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=chrome_options
    )

    url = "https://juris.pjud.cl/busqueda?Sentencias_Penales"
    driver.get(url)
    time.sleep(10)  # Esperar a que la página cargue

    total_pages = 2
    all_sentences = []
    start_time = time.time()  # Tiempo inicial

    for page in range(total_pages):
        page_start_time = time.time()
        print(f"\n📄 Scrapeando página {page + 1} de {total_pages}...")

        sentences_data = []
        results = driver.find_elements(By.CLASS_NAME, "card.border-info")

        for result in results:
            sentencia = {}

            # Extraer rol
            try:
                rol = result.find_element(By.XPATH, ".//span[contains(text(), 'ROL:')]")
                sentencia["rol"] = rol.text.split("ROL:")[-1].strip() if rol else None
            except:
                sentencia["rol"] = None

            # Extraer caratulado
            try:
                caratulado = result.find_element(By.XPATH, ".//span[contains(text(), 'Caratulado:')]")
                sentencia["caratulado"] = caratulado.text.split("Caratulado:")[-1].strip() if caratulado else None
            except:
                sentencia["caratulado"] = None

            # Extraer fecha, asignar fecha actual si no está presente
            try:
                fecha = result.find_element(By.XPATH, ".//span[contains(text(), 'Fecha:')]")
                sentencia["fecha"] = fecha.text.split("Fecha:")[-1].strip() if fecha else datetime.now().strftime("%Y-%m-%d")
            except:
                sentencia["fecha"] = datetime.now().strftime("%Y-%m-%d")  # Valor por defecto

            # Extraer tribunal, asignar valor vacío si no está presente
            try:
                tribunal = result.find_element(By.XPATH, ".//span[contains(text(), 'Tribunal:')]")
                sentencia["tribunal"] = tribunal.text.split("Tribunal:")[-1].strip() if tribunal else ""
            except:
                sentencia["tribunal"] = ""

            # Extraer materia, asignar valor vacío si no está presente
            try:
                materia = result.find_element(By.XPATH, ".//span[contains(text(), 'Materia:')]")
                sentencia["materia"] = materia.text.split("Materia:")[-1].strip() if materia else ""
            except:
                sentencia["materia"] = ""

            # Extraer juez, asignar valor vacío si no está presente
            try:
                juez = result.find_element(By.XPATH, ".//span[contains(text(), 'Juez:')]")
                sentencia["juez"] = juez.text.split("Juez:")[-1].strip() if juez else ""
            except:
                sentencia["juez"] = ""

            # Extraer enlace, asignar valor vacío si no está presente
            try:
                enlace = result.find_element(By.XPATH, ".//a[contains(text(), 'Ver Sentencia')]")
                sentencia["enlace"] = enlace.get_attribute('href') if enlace else ""
            except:
                sentencia["enlace"] = ""

            sentences_data.append(sentencia)

        all_sentences.extend(sentences_data)

        elapsed_time = time.time() - start_time
        avg_time_per_page = elapsed_time / (page + 1)
        remaining_time = avg_time_per_page * (total_pages - (page + 1))

        print(f"✅ Página {page + 1} completada en {round(time.time() - page_start_time, 2)}s")
        print(f"⏳ Tiempo estimado restante: {timedelta(seconds=int(remaining_time))}")

        try:
            next_button = driver.find_element(By.ID, "btnPaginador_pagina_adelante")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
        except:
            print(f"⚠️ No se encontró el botón para la página {page + 2}, deteniendo.")
            break

    driver.quit()
    return all_sentences

def save_sentences_to_db(sentences_data):
    db = SessionLocal()
    for data in sentences_data:
        if data.get("rol") is not None:
            db.add(Sentencia(**data))
    db.commit()
    db.close()

async def scrape_and_save_data():
    sentences_data = fetch_data()
    save_sentences_to_db(sentences_data)
    print(f"🎉 Scrapeo completo. Se guardaron {len(sentences_data)} sentencias.")
