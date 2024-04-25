#Este Script solamente utiliza la pagina web manhwaweb. 
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import uvicorn

app = FastAPI()

# Configurar el PDF
pdf_path = "/home/samuelmf98/task_api_manga/mangas.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4  # A4 size

@app.get("/generar_pdf/")
async def generar_pdf(capitulo_inicio: int, capitulo_final: int):
    # Configure PDF saving for each chapter
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4  # A4 size

    for i in range(capitulo_inicio, capitulo_final + 1):
        try:
            url = f"https://manhwaweb.com/leer/sousou-no-frieren_1696233652704-{i}"
            # Configurar el servicio del driver de Chrome y las opciones del navegador
            print("Configurando el navegador...")
            options = Options()
            options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin ventana)
            with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                print(f"Accediendo a {url}...")
                driver.get(url)

                # Esperar a que las imágenes se carguen
                print("Esperando a que desaparezca el GIF de carga...")
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[src*='cargando']"))
                )

                # Obtener el HTML y procesarlo con BeautifulSoup
                print("Procesando el contenido del capitulo {}".format(i))
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # Buscar todas las etiquetas <img> y extraer las URLs de las imágenes
                print("Buscando imágenes del capitulo {}".format(i))
                image_elements = soup.find_all('img')
                image_urls = [img['src'] for img in image_elements if img['src'].endswith('.jpg')]

                if image_urls:
                    print(f"Se encontraron {len(image_urls)} imágenes .jpg.")
                    for image_url in image_urls:
                        print(f"Descargando imagen: {image_url}")
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_file = BytesIO(response.content)
                            image = Image.open(image_file)
                            if image.mode == 'RGBA':
                                image = image.convert('RGB')
                            image_width = width
                            image_height = int(image_width * (image.size[1] / image.size[0]))
                            c.drawInlineImage(image, 0, height - image_height, image_width, image_height)
                            c.showPage()
                        else:
                            print(f"Error al descargar la imagen: {image_url}")
                else:
                    print("No se encontraron imágenes .jpg válidas.")

        except Exception as e:
            print("Ocurrió un error durante la ejecución del script:")
            print(e)
            raise HTTPException(status_code=500, detail=f"Error interno al procesar el capítulo {i}")

    c.save()
    print(f"PDF guardado en {pdf_path}")
    print("Script finalizado.")
    return {"message": "PDF generado con éxito", "path": pdf_path}

# Añadir ejecución de Uvicorn directamente en el script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
