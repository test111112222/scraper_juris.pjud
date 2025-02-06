from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from .database import SessionLocal
from .models import Sentencia

def fetch_data():
    # Configurar Selenium para usar el servicio remoto en Docker
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",  # URL del servicio Selenium en Docker
        options=chrome_options
    )

    url = "https://juris.pjud.cl/busqueda?Sentencias_Penales"
    driver.get(url)

    # Esperar 10 segundos para que cargue la página completamente
    time.sleep(10)

    # Extraer datos con Selenium
    sentences_data = []
    results = driver.find_elements(By.CLASS_NAME, "card.border-info")

    for result in results:
        sentencia = {}

        try:
            rol = result.find_element(By.XPATH, ".//span[contains(text(), 'ROL:')]")
            sentencia["rol"] = rol.text.split("ROL:")[-1].strip() if rol else None
        except:
            sentencia["rol"] = None

        try:
            caratulado = result.find_element(By.XPATH, ".//span[contains(text(), 'Caratulado:')]")
            sentencia["caratulado"] = caratulado.text.split("Caratulado:")[-1].strip() if caratulado else None
        except:
            sentencia["caratulado"] = None

        sentences_data.append(sentencia)

    driver.quit()
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