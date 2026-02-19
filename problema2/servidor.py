#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Servidor
Objetivo: Crear un servidor TCP que devuelva exactamente lo que recibe del cliente
"""

import socket

# TODO: Definir la dirección y puerto del servidor
HOST = "localhost"
PORT = 9000

# Crear un socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
servidor = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#: Enlazar el socket a la dirección y puerto especificados
servidor.bind((HOST, PORT))

# Poner el socket en modo escucha
servidor.listen(1)
# El parámetro define el número máximo de conexiones en cola
print("servidor iniciando en", HOST, "en el puerto", PORT)

# Bucle infinito para manejar múltiples conexiones (una a la vez)
while True:

    print("Servidor a la espera de conexiones ...")
    
    # Aceptar una conexión entrante
    conn, addr = servidor.accept()
     print(f"Conexión realizada por {addr}")
    # accept() bloquea hasta que llega una conexión
    # conn: nuevo socket para comunicarse con el cliente
    # addr: dirección y puerto del cliente
    
    try:

    # Recibir datos del cliente (hasta 1024 bytes)
       data =conn.recv(1024)
    # Si no se reciben datos, salir del bucle
    if not data:
        break

    # Mostrar los datos recibidos (en formato bytes)
   mensaje =data.decode("utf-8")
   print("mensaje recibido del cliente:",mensaje)

    
    #  Enviar los mismos datos de vuelta al cliente (echo)
    conn.sendall(data)
    print("mensaje enviado de vuelta al cliente.")
    
    # Cerrar la conexión con el cliente actual
    conn.close()
    print("conexion cerrada con el cliente", addr)

