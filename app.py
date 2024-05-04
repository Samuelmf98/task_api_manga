from fastapi import FastAPI, HTTPException
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import uvicorn

from extraer_url import buscar_primer_capitulo
from generar_pdf import fetch_chapter_images
from http_requests import requests_retry_session
from extract_manga_name import extract_manga_name

app = FastAPI()



@app.get("/generar_pdf/")
async def generar_pdf(capitulo_inicio: int, capitulo_final: int, nombre_manga: str): 
    session = requests_retry_session()

    url_original= buscar_primer_capitulo(nombre_manga) #Extraemos la URL original utilizando el nombre del manga que el usuario introduce.
    print("Esta es la URL original:")
    print(url_original)

    original_manga_name = extract_manga_name(url_original) #A partir de esta URL extraemos el nombre original del manga.
    print("Se ha extraído este nombre de manga")
    print(original_manga_name)

    pdf_path = f"/home/samuelmf98/task_api_manga_cascada/mangas/{original_manga_name}_{capitulo_inicio}_{capitulo_final}.pdf"
    width, height = A4  # A4 size
    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Factor de escala para las imágenes (0.75 significa 75% del tamaño original)
    scale_factor = 0.75

    for capitulo in range(capitulo_inicio, capitulo_final + 1):
        pagina = 1
        imagenes_encontradas = False  # Indicador de si se han encontrado imágenes
        while True:  # Iteramos indefinidamente hasta que no haya más páginas
       
            try:
                url = f"{url_original}/{capitulo}/{pagina}"
                image_urls = fetch_chapter_images(url,capitulo)
                

                if not image_urls:
                    if not imagenes_encontradas:  # Solo imprime el mensaje si es el primer intento
                        print("No se han encontrado imágenes del capitulo {}".format(capitulo))
                    break

                imagenes_encontradas = True 
                for image_url in image_urls:
                    print("Descargando imagen {} del capitulo {}".format((image_url), (capitulo)))
                    response = session.get(image_url)
                    if response.status_code == 200:
                        image_file = BytesIO(response.content)
                        image = Image.open(image_file)

                        if image.mode == 'RGBA':
                            image = image.convert('RGB')
                        
                         # Convertir de WEBP a JPEG en memoria
                        image_bytes_io = BytesIO()
                        image.save(image_bytes_io, format='JPEG')
                        image_bytes_io.seek(0)
                        image = Image.open(image_bytes_io)
                        
                        image_width = width * scale_factor
                        image_height = int(image_width * (image.size[1] / image.size[0]))
                        c.drawInlineImage(image, 0, height - image_height, image_width, image_height)
                        c.showPage()
                        image_file.close()
                    else:
                        print(f"Error al descargar la imagen: {image_url}")
                pagina += 1
        
            
            except Exception as e:
                print("Ocurrió un error durante la ejecución del script:")
                print(e)
                traceback.print_exc()  # Imprime el traceback para diagnosticar mejor
                raise HTTPException(status_code=500, detail=f"Error interno al procesar el capítulo {capitulo}")

    c.save()
    print(f"PDF guardado en {pdf_path}")
    return {"message": "PDF generado con éxito", "path": pdf_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")