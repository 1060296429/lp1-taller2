#!/usr/bin/env python3

import socket
import threading

BUFFER_SIZE = 4096
LISTEN_PORT = 8888   # Puerto del proxy


def forward(src, dst):
    """Reenvía datos entre dos sockets."""
    try:
        while True:
            data = src.recv(BUFFER_SIZE)
            if not data:
                break
            dst.sendall(data)
    except:
        pass
    finally:
        src.close()
        dst.close()


def handle_https(client_socket, target_host, target_port):
    """Maneja túnel HTTPS (método CONNECT)."""
    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((target_host, target_port))

        # Respuesta al navegador: túnel establecido
        client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

        # Comunicación bidireccional
        threading.Thread(target=forward, args=(client_socket, remote)).start()
        threading.Thread(target=forward, args=(remote, client_socket)).start()

    except Exception as e:
        print("Error HTTPS:", e)
        client_socket.close()


def handle_http(client_socket, request):
    """Maneja peticiones HTTP normales (GET, POST, etc)."""
    try:
        lines = request.split(b"\r\n")
        first_line = lines[0].decode()

        method, url, protocol = first_line.split()

        # Extraer host
        host = None
        port = 80

        for line in lines:
            if line.lower().startswith(b"host:"):
                host = line.split(b":")[1].strip().decode()
                if ":" in host:
                    host, port = host.split(":")
                    port = int(port)
                break

        if not host:
            client_socket.close()
            return

        # Conectar al servidor real
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((host, port))

        # Reenviar petición
        remote.sendall(request)

        # Enviar respuesta al cliente
        while True:
            data = remote.recv(BUFFER_SIZE)
            if not data:
                break
            client_socket.sendall(data)

        remote.close()
        client_socket.close()

    except Exception as e:
        print("Error HTTP:", e)
        client_socket.close()


def handle_client(client_socket, addr):
    """Maneja cada cliente conectado."""
    print(f"Cliente conectado: {addr}")

    try:
        request = client_socket.recv(BUFFER_SIZE)

        if not request:
            client_socket.close()
            return

        # Verificar si es HTTPS
        if request.startswith(b"CONNECT"):
            line = request.split(b"\r\n")[0]
            target = line.split()[1].decode()
            host, port = target.split(":")
            port = int(port)

            print(f"Tunel HTTPS -> {host}:{port}")
            handle_https(client_socket, host, port)
        else:
            print("Petición HTTP detectada")
            handle_http(client_socket, request)

    except Exception as e:
        print("Error cliente:", e)
        client_socket.close()


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", LISTEN_PORT))
    server.listen(100)

    print(f"Proxy escuchando en puerto {LISTEN_PORT}...")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()


if __name__ == "__main__":
    start_proxy()