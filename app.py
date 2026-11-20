import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET

import requests


# Direccion web donde el BCE publica cada dia los tipos de cambio en XML
URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


# ---------------------------------------------------------------
# 1. API: descargar el XML de Internet
# ---------------------------------------------------------------
def descargar_xml():
    """Hace una peticion GET a la URL del BCE y devuelve el texto del XML.
    Si algo falla devuelve None."""
    try:
        respuesta = requests.get(URL_BCE, timeout=10)

        # El codigo 200 significa que el servidor ha respondido correctamente
        if respuesta.status_code == 200:
            return respuesta.content.decode("utf-8")
        else:
            print("Error al conectar con el servidor:", respuesta.status_code)
            return None

    except Exception as e:
        # Entra aqui si no hay Internet, la web no responde, etc.
        print(f"Ha ocurrido un error: {e}")
        return None


# ---------------------------------------------------------------
# 2. XML: sacar la fecha y las monedas con sus tasas
# ---------------------------------------------------------------
def leer_xml(texto_xml):
    """Recorre el XML y devuelve dos cosas:
    - la fecha de los datos (atributo time)
    - un diccionario {moneda: tasa} (atributos currency y rate)"""

    # Convierte el texto en un arbol de elementos que podemos recorrer
    raiz = ET.fromstring(texto_xml)

    fecha = ""
    tasas = {}

    # El Euro no viene en el XML porque todas las tasas son respecto a el asi que lo añadimos
    tasas["EUR"] = 1.0

    # iter() pasa por todos los elementos del arbol, uno a uno
    for elemento in raiz.iter():

        # El Cube que tiene el atributo "time" guarda la fecha
        if elemento.get("time") is not None:
            fecha = elemento.get("time")

        # Los Cube que tienen "currency" guardan una moneda y su tasa
        if elemento.get("currency") is not None:
            moneda = elemento.get("currency")
            tasa = float(elemento.get("rate"))  # el rate viene como texto, lo pasamos a numero
            tasas[moneda] = tasa

    return fecha, tasas


# ---------------------------------------------------------------
# 3. Matematicas: conversion usando el Euro como puente
# ---------------------------------------------------------------
def convertir(importe, tasa_origen, tasa_destino):
    """Primero pasa el importe a euros (dividiendo por la tasa de origen)
    y despues de euros a la moneda destino (multiplicando por su tasa)."""
    en_euros = importe / tasa_origen
    return en_euros * tasa_destino


# ---------------------------------------------------------------
# 4. GUI: la ventana con Tkinter
# ---------------------------------------------------------------
def boton_calcular():
    """Se ejecuta cuando el usuario pulsa el boton Convertir."""

    # Leemos lo que ha escrito el usuario. Cambiamos la coma por punto
    # para que "10,5" tambien funcione
    texto = entrada_cantidad.get().replace(",", ".")

    # Validacion: si no es un numero, float() da error y avisamos
    try:
        cantidad = float(texto)
    except ValueError:
        messagebox.showerror("Error", "Introduce un numero valido en la cantidad.")
        return

    origen = combo_origen.get()
    destino = combo_destino.get()

    resultado = convertir(cantidad, tasas[origen], tasas[destino])

    # Mostramos el resultado con 2 decimales
    etiqueta_resultado.config(text=f"{cantidad:.2f} {origen} = {resultado:.2f} {destino}")


# --- Carga automatica de datos al arrancar el programa ---
texto_xml = descargar_xml()

if texto_xml is None:
    # Sin datos no podemos convertir nada, asi que avisamos y cerramos
    messagebox.showerror("Error", "No se han podido descargar los datos del BCE.")
    raise SystemExit

fecha, tasas = leer_xml(texto_xml)

# Lista de monedas ordenada alfabeticamente para los desplegables
lista_monedas = sorted(tasas.keys())


# --- Creacion de la ventana ---
ventana = tk.Tk()
ventana.title("Conversor de monedas Pol")
ventana.geometry("380x300")
ventana.configure(bg="#492561")

# Colores y letra que se reutilizan en varios elementos
COLOR_FONDO = "#492561"
COLOR_TEXTO = "#edf2f4"
LETRA = ("Consolas", 11)

# Titulo
tk.Label(ventana, text="Conversor de monedas", bg=COLOR_FONDO, fg="#ffb703",
         font=("Consolas", 16, "bold")).pack(pady=10)

# Fecha de actualizacion sacada del XML
tk.Label(ventana, text=f"Tipos de cambio del dia: {fecha}", bg=COLOR_FONDO,
         fg=COLOR_TEXTO, font=LETRA).pack()

# Frame = contenedor para colocar los campos en forma de tabla (grid)
marco = tk.Frame(ventana, bg=COLOR_FONDO)
marco.pack(pady=15)

# Campo para escribir la cantidad
tk.Label(marco, text="Cantidad:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=LETRA).grid(row=0, column=0, sticky="w", pady=4)
entrada_cantidad = tk.Entry(marco, width=15, font=LETRA)
entrada_cantidad.grid(row=0, column=1, pady=4)

# Desplegable de la moneda de origen (state="readonly" impide escribir dentro)
tk.Label(marco, text="Moneda origen:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=LETRA).grid(row=1, column=0, sticky="w", pady=4)
combo_origen = ttk.Combobox(marco, values=lista_monedas, state="readonly", width=13)
combo_origen.grid(row=1, column=1, pady=4)

# Desplegable de la moneda de destino
tk.Label(marco, text="Moneda destino:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=LETRA).grid(row=2, column=0, sticky="w", pady=4)
combo_destino = ttk.Combobox(marco, values=lista_monedas, state="readonly", width=13)
combo_destino.grid(row=2, column=1, pady=4)

# Boton que llama a la funcion boton_calcular al pulsarlo
tk.Button(ventana, text="Convertir", command=boton_calcular, bg="#ffb703",
          fg="#2b2d42", font=("Consolas", 11, "bold"), width=12).pack()

# Etiqueta donde se escribe el resultado (empieza vacia)
etiqueta_resultado = tk.Label(ventana, text="", bg=COLOR_FONDO, fg="#8ecae6",
                              font=("Consolas", 12, "bold"))
etiqueta_resultado.pack(pady=15)

# mainloop() mantiene la ventana abierta esperando a que el usuario haga algo
ventana.mainloop()
