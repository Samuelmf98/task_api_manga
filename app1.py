from fastapi import FastAPI, HTTPException
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import traceback

from extraer_url import buscar_primer_capitulo
from generar_pdf import fetch_chapter_images
from http_requests import requests_retry_session
from extract_manga_name import extract_manga_name

import asyncio
import aiohttp

app = FastAPI()

async def download_image_async(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            return Image.open(BytesIO(await response.read()))
        else:
            print(f"Error al descargar la imagen: {url}")
    return None

@app.get("/generar_pdf/")
async def generar_pdf(capitulo_inicio: int, capitulo_final: int, nombre_manga: str):
    url_original= buscar_primer_capitulo(nombre_manga) #Extraemos la URL original utilizando el nombre del manga que el usuario introduce.
    print("Esta es la URL original:")
    print(url_original)

    original_manga_name = extract_manga_name(url_original) #A partir de esta URL extraemos el nombre original del manga.
    print("Se ha extraído este nombre de manga")
    print(original_manga_name)
    pdf_path = f"/home/samuelmf98/task_api_manga_cascada/mangas/{original_manga_name}_{capitulo_inicio}_{capitulo_final}.pdf"
    width, height = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)

    async with aiohttp.ClientSession() as session:
        for capitulo in range(capitulo_inicio, capitulo_final + 1):
            pagina = 1
            while True:
                url = f"{url_original}/{capitulo}/{pagina}"
                image_urls = fetch_chapter_images(url, capitulo)
                if not image_urls:
                    break

                tasks = [download_image_async(url, session) for url in image_urls]
                images = await asyncio.gather(*tasks)

                for image in filter(None, images):
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    image_width = width
                    image_height = int(image_width * (image.size[1] / image.size[0]))
                    c.drawInlineImage(image, 0, height - image_height, image_width, image_height)
                    c.showPage()

                pagina += 1

    c.save()
    return {"message": "PDF generado con éxito", "path": pdf_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")