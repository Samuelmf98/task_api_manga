'''Esta función accede al navegador utilizando la URL original y un capítulo por el que iterar.
Espera a que la página cargue completamente para garantizar que el código HTML esté disponible
y poder encontrar todas los archivos webp. Es decir, las imágenes de nuestro capítulo.
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

async def fetch_chapter_images(url,capitulo_numero):
    #print("Configurando el navegador...")
    options = Options()
    options.add_argument("--headless")
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        #print(f"Accediendo a {url}...")
        driver.get(url)
        #print("Esperando a que desaparezca el GIF de carga...")
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[src*='cargando']"))
        )
        #print("Procesando el contenido del capitulo {}".format(capitulo_numero))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #print("Buscando imágenes del capitulo {}".format(capitulo_numero))
        image_elements = soup.find_all('img')
        return [img['src'] for img in image_elements if img['src'].endswith('.webp')]