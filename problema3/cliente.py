#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Cliente
Objetivo: Crear un cliente de chat que se conecte a un servidor y permita enviar/recibir mensajes en tiempo real
"""

import socket
import threading
HOST ="localhost"
PORT = 9000

def receive_messages():
   # Función ejecutada en un hilo separado para recibir mensajes del servidor
    #de forma continua sin bloquear el hilo principal.
    while True:
        try:
            # Recibir mensajes del servidor (hasta 1024 bytes) y decodificarlos
            message = client_socket.recv(1024)
        if not message:
            print("Error al recibir mensaje del servidor")
            break

        # Imprimir el mensaje recibido
        print(message.decode('utf-8'))
        print("\n+ mensaje")
        except:
            print("Error al recibir mensaje del servidor")
            client.close()
            break
# Solicitar nombre de usuario al cliente
client_name = input("Cuál es tu nombre? ")

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

#  Conectar el socket al servidor en la dirección y puerto especificados
client_socket.connect((HOST, PORT))

# Enviar el nombre del cliente al servidor (codificado a bytes)
client_socket.send(client_name.encode('utf-8'))

# Crear y iniciar un hilo para recibir mensajes del servidor
# target: función que se ejecutará en el hilo
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True #permite que el hilo se cierre automaticamente cuando el programa principal termine
receive_thread.start()

# Bucle principal en el hilo principal para enviar mensajes al servidor
while True:
    try:
         message = input()
if message.lower() == "salir":
    client_socket.close()
    break
    # Solicitar mensaje al usuario por consola
   full_mensaje = f"{client_name}: {message}"
    # : Codificar el mensaje a bytes y enviarlo al servidor
    client_socket.send(full_mensaje.encode('utf-8'))
    except:
        print("Error al enviar mensaje al servidor")
        client_socket.close()
        break