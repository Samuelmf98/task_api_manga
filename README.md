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

El programa aun no esta preparado para ejecutarse fuera del localhost.
