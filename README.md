# Nombre del Proyecto

Descripción breve del proyecto.

## Pre-requisitos

Asegúrate de tener instalado Google Chrome en tu sistema. Si estás usando un entorno basado en Debian/Ubuntu, puedes instalarlo con:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb' 
```
## Creación del Entorno Virtual

Crear un entorno virtual en Python te permite gestionar las dependencias del proyecto de forma aislada. Esto es especialmente útil para evitar conflictos entre las bibliotecas requeridas por diferentes proyectos. Aquí te explicamos cómo crear y activar un entorno virtual:

1. **Crear el entorno virtual**:
   Ejecuta el siguiente comando en tu terminal. Esto creará un nuevo directorio `venv` en tu proyecto, donde se almacenarán las dependencias.

```bash
   python3 -m venv venv
   ```

2. **Iniciar el entorno virtual**:
   Ejecutar el comando:
   
   ``bash
   source venv/bin/activate
   ```
2. **Instalar las librerias necesarias**:
   Ejecutar el comando:

    ``bash
   pip install -r requirements.txt
   ```
