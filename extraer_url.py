'''Las URL a las que tenemos que acceder no son muy obvias ya que están hashed, por tanto, cambian continuamente.
Esta funcion recoge el nombre del manga que la persona quiere leer y realiza una busqueda en internet a una página específica para recoger la URL
'''

from googlesearch import search

def buscar_primer_capitulo(anime):
    query = f"visortmo.ws leer manga {anime}" #esta es la búsqueda. Utilizamos palabras clave para optimizar la búsqueda.
    # Realiza la búsqueda en Google y obtiene los resultados como un generador
    search_results = search(query, num_results=1)

    # Intenta obtener el primer resultado del generador
    try:
        first_result_url = next(search_results)
        first_result_url_no_processed = first_result_url.replace("leer", "manga")
        print(f"URL sin procesar de '{anime}': {first_result_url_no_processed}")

        '''En algunas ocasiones el URL accede directamente a un capítulo.
            Como no queremos eso eliminamos el capítulo de la URL'''
        last_dash_index = first_result_url_no_processed.rfind('-')

        if last_dash_index >= len(first_result_url_no_processed) - 5:
            # Cortar el string hasta el guión
            first_result_url_processed = first_result_url_no_processed[:last_dash_index]
            print(f"URL procesada de '{anime}': {first_result_url_processed}")
            return first_result_url_processed
        return first_result_url_no_processed
    except StopIteration:
        print("No se encontraron resultados de {}".format(anime))
        return None
