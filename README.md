# Conversor de Divisas

Aplicación en Python que descarga los tipos de cambio del Banco Central Europeo (XML),
los lee con `xml.etree.ElementTree` y permite convertir entre monedas desde una ventana hecha con Tkinter.

## Requisitos

- Tener instalado **Python 3** (https://www.python.org/downloads/). En Windows, al instalarlo marcar la casilla **"Add Python to PATH"**.
- Tener instalado **Git** (https://git-scm.com/downloads), solo si se descarga con la opción A.
- Conexión a Internet, porque el programa descarga los datos del BCE al arrancar.

## Cómo descargarlo y ejecutarlo

### 1. Descargar el proyecto

**Opción A: con Git**

Abrir una terminal en la carpeta donde se quiera guardar el proyecto y ejecutar:

```
git clone https://github.com/polcanros/Conversor-de-Divisas-ejercicio.git
cd Conversor-de-Divisas-ejercicio
```

**Opción B: sin Git**

1. En la página del repositorio pulsar el botón verde **Code** y luego **Download ZIP**.
2. Descomprimir el ZIP.
3. Abrir una terminal dentro de la carpeta descomprimida.

### 2. Crear el entorno virtual

El entorno virtual (`venv`) es una carpeta donde se instalan las librerías solo para este proyecto.

```
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows:

```
venv\Scripts\activate
```

En Mac / Linux:

```
source venv/bin/activate
```

Cuando está activado aparece `(venv)` al principio de la línea de la terminal.

> Si en Windows PowerShell da un error de "ejecución de scripts deshabilitada", ejecutar antes
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y volver a intentarlo.

### 4. Instalar las librerías necesarias

```
pip install -r requirements.txt
```

Esto instala `requests`, que es la librería que se usa para descargar el XML.

### 5. Ejecutar el programa

```
python app.py
```

Se abrirá la ventana del conversor con los tipos de cambio del día.
