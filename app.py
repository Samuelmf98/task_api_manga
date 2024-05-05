from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import asyncio
import os
import time

from extraer_url import buscar_primer_capitulo
from generar_pdf import fetch_chapter_images
from http_requests import aiohttp_retry_session
from extract_manga_name import extract_manga_name

class PdfRequest(BaseModel):
    capitulo_inicio: int
    capitulo_final: int
    nombre_manga: str



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #// Permitir todos los orígenes para desarrollo
    allow_methods=["*"],  #// Permitir todos los métodos
    allow_credentials=True, 
    allow_headers=["*"],  #// Permitir todos los headers
)

def remove_file_later(path: str):
    """ Espera un tiempo antes de intentar eliminar el archivo, asegurando que la respuesta ha sido completamente enviada. """
    time.sleep(10)  # Espera 10 segundos antes de eliminar el archivo
    if os.path.exists(path):
        os.remove(path)
        print(f"Archivo {path} eliminado correctamente.")
    else:
        print(f"Archivo {path} no encontrado para eliminar.")


@app.post("/generar_pdf/")
async def generar_pdf(request: PdfRequest, background_tasks: BackgroundTasks): 
     async with await aiohttp_retry_session() as session:
        url_original = buscar_primer_capitulo(request.nombre_manga)
        original_manga_name = extract_manga_name(url_original)
        pdf_path = f"/tmp/{original_manga_name}_{request.capitulo_inicio}_{request.capitulo_final}.pdf"
        width, height = A4  # A4 size
        c = canvas.Canvas(pdf_path, pagesize=A4)
        scale_factor = 0.75

        for capitulo in range(request.capitulo_inicio, request.capitulo_final + 1):
            pagina = 1
            imagenes_encontradas = False
            while True:
                url = f"{url_original}/{capitulo}/{pagina}"
                image_urls = await fetch_chapter_images(url, capitulo)
                if not image_urls:
                    print("No se han encontrado imágenes del capitulo {}".format(capitulo))
                    break
                imagenes_encontradas = True 

                images = await fetch_images_asynchronously(image_urls, session)

                for image_data in images:
                    print(f"Descargando y procesando imagen {pagina} del capítulo {capitulo}")
                    image = Image.open(BytesIO(image_data))
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    
                    image_bytes_io = BytesIO()
                    image.save(image_bytes_io, format='JPEG')
                    image_bytes_io.seek(0)
                    image = Image.open(image_bytes_io)

                    image_width = width * scale_factor
                    image_height = int(image_width * (image.size[1] / image.size[0]))
                    c.drawInlineImage(image, 0, height - image_height, image_width, image_height)
                    c.showPage()

                pagina += 1

                # Agrega la tarea de eliminación del archivo en segundo plano
        background_tasks.add_task(remove_file_later, pdf_path)

        c.save()
        print(f"PDF guardado en {pdf_path}")
        return FileResponse(
            path=pdf_path,
            headers={"Content-Disposition": f"attachment; filename={original_manga_name}_{request.capitulo_inicio}_{request.capitulo_final}.pdf"},
            media_type='application/pdf'
        )



async def fetch_images_asynchronously(image_urls, session):
    tasks = [session.get(image_url) for image_url in image_urls]
    responses = await asyncio.gather(*tasks)  # Now asyncio is defined and this should work
    images = [await resp.read() for resp in responses if resp.status == 200]
    return images


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")