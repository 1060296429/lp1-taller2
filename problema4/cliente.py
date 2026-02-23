#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""

import http.client

#  Definir la dirección y puerto del servidor HTTP 
HOST = "localhost"
PORT = 8000 #puerto comun para servidores HTTP locales 

# : Crear una conexión HTTP con el servidor
conexion =http.client.HTTPConnection(HOST, PORT)
try:
    print("conectando al servidor ...")
# Realizar una petición GET al path raíz ('/')
conexion.request("GET", "/")
# request() envía la petición HTTP al servidor
# Primer parámetro: método HTTP (GET, POST, etc.)
# Segundo parámetro: path del recurso solicitado

# Obtener la respuesta del servidor
# devuelve un objeto HTTPResponse con los datos de la respuesta
respuesta = conexion.getresponse()
print("estado de la respuesta:", respuesta.status)
print("razon de la respuesta:", respuesta.reason)

# : Leer el contenido de la respuesta
datos = respuesta.read()#devuelve el cuerpo de la respuesta en bytes

#  Decodificar los datos de bytes a string e imprimirlos
contenido = datos.decode()
print("\n contenido de la respuesta UTF-8", contenido)
print(contenido)
# decode() convierte los bytes a string usando UTF-8 por defecto
finally:
#Cerrar la conexión con el servidor
conexion.close()
print("conexion cerrada")
