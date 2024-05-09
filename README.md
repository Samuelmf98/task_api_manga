# Descripción breve del proyecto.

El objetivo de este proyecto es crear un programa que descargue capitulos de mangas y los añada a un pdf, el cual puede ser leído tanto en un pc como  en un móvil, mejorando de esta forma, la fluidez de la lectura y dando la posibilidad de leer mangas sin tener conexión a internet, como por ejemplo, en vuelos de larga duración.

## Creación del Entorno Virtual

Crear un entorno virtual en Python te permite gestionar las dependencias del proyecto de forma aislada. Esto es especialmente útil para evitar conflictos entre las bibliotecas requeridas por diferentes proyectos. Aquí te explicamos cómo crear y activar un entorno virtual:

1. **Crear el entorno virtual**:
   Ejecuta el siguiente comando en tu terminal. Esto creará un nuevo directorio `venv` en tu proyecto, donde se almacenarán las dependencias.

   ```bash
      python3 -m venv venv
      ```
2. **Activar Entorno Virtual**

   ```bash
      source venv/bin/activate
      ```
3. **Instalar requirements**
   Asegúrate de tener instalado Google Chrome en tu sistema. Si estás usando un entorno basado en Debian/Ubuntu, puedes instalarlo con:
   ```bash
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt install ./google-chrome-stable_current_amd64.deb' 
   ```
   Una vez hecho esto, instalamos lss librerías necesarias. Para ello ejecutamos el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del programa

Para usar el programa ejecutamos el siguiente código:
```bash
   python3 app.py
   ```
Axto seguido accedemos al navegador web y entramos en la siguiente url:

http://localhost:8000/docs

En esta página seleccionamos *Try it out* y acto seguido rellenamos los campos especificados. Por ejemplo, si quieres leer el manga One Piece del capítulo 30 al 45, deberás rellenar los 3 campos de la siguiente forma:

*nombre_manga:* One piece

*capitulo_inicio:* 30

*capitulo_final:* 45

Finalmente seleecionamos *Execute* y veremos en la terminal cómo automáticamente se descagran las imágenes de cada capítulo para añadirlos a un pdf, el cual al finalizar el proceso estará disponible en la localización especificada.

```
<link rel="icon" href="favicon.ico" type="image/x-icon">
```
python -m http.server 8001
python3 app.py 

ngrok start --all --config ngrok.yml
