#!/usr/bin/env python3

Problema 3: Chat simple con múltiples clientes - Servidor
Objetivo: Crear un servidor de chat que maneje múltiples clientes simultáneamente usando threads

import socket
import threading

HOST = "localhost"
PORT = 9000

# Crear socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Evita error: reiniciar el servidor rapidamente
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enlazar y escuchar
server.bind((HOST, PORT))
server.listen(5)

print("Servidor de chat iniciando...")

# Listas globales
clients = []
names = []

# ENVIAR A TODOS MENSAJES A LOS QUE ESTAN CONECTADOS
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

# MANEJAR CLIENTE 
def handle_client(client_socket, addr):

    try:
        # Recibir nombre
        name = client_socket.recv(1024)

        names.append(name)
        clients.append(client_socket)

        print(f"{name} conectado desde {addr}")

        broadcast(f"{name} se ha unido al chat.\n".encode('utf-8'))

        # Escuchar mensajes
        while True:
            message = client_socket.recv(1024)

            if not message:
                break

            print(message.decode('utf-8'))

            # reenviar a todos
            broadcast(message, client_socket)

    except:
        pass

    finally:
        # eliminar cliente al salir
        if client_socket in clients:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            name = names[index]
            names.remove(name)

            print(f"{name} desconectado")
            broadcast(f"{name} salió del chat.\n".encode('utf-8'))

        client_socket.close()


# ACEPTAR CONEXIONES
while True:
    print("Esperando clientes...")
    client_socket, addr = server.accept()

    # crear hilo por cliente
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.daemon = True
    thread.start()

