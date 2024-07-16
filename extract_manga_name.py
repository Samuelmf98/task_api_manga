'''Para nombrar el PDF final necesitamos el nombre original del manga.
No podemos utilizar el nombre que el usuario introduce porque este puede contener faltas ortográficas.
Utilizamos esta función para extraer el nombre correcto a partir de la URL original.
'''
def extract_manga_name(url):
    # Divide la URL en partes basándose en '/'
    parts = url.split('/')
    print("parts: {}".format(parts))
    
    # Encuentra el segmento que contiene 'manga' y toma el siguiente segmento
    manga_name = None  # Inicializa la variable manga_name
    for i, part in enumerate(parts):
        if part == 'manga' and i + 1 < len(parts):  # Asegura que 'manga' sea parte y no sea el último segmento
            manga_part = parts[i + 1]  # Toma el siguiente segmento después de 'manga'
            print("Segmento encontrado después de 'manga': {}".format(manga_part))
            # Ahora divide este segmento en partes basadas en '_' y toma el primer elemento
            manga_name = manga_part.split('_')[0]
            break  # Sale del bucle una vez encontrado el nombre
    
    if manga_name is None:
        print("No se encontró el segmento 'manga' en la URL o está en la última posición.")
        return None  # O podrías manejarlo de otra manera dependiendo de tus necesidades

    return manga_name

    