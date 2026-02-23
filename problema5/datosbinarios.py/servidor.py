
import socket
import os
import hashlib
import threading

HOST = '0.0.0.0'
PORT = 9001
BUFFER_SIZE = 4096
BASE_DIR = "storage"

def safe_path(filename):
    # Evita path traversal
    return os.path.join(BASE_DIR, os.path.basename(filename))

def checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BUFFER_SIZE), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode().strip()
        if not command:
            break

        if command.startswith("UPLOAD"):
            _, filename = command.split()
            filepath = safe_path(filename)
            with open(filepath, "wb") as f:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if data == b"EOF":
                        break
                    f.write(data)
            conn.send(checksum(filepath).encode())

        elif command.startswith("DOWNLOAD"):
            _, filename = command.split()
            filepath = safe_path(filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(BUFFER_SIZE), b""):
                        conn.send(chunk)
                conn.send(b"EOF")
                conn.send(checksum(filepath).encode())
            else:
                conn.send(b"ERROR: File not found")

        elif command == "LIST":
            files = os.listdir(BASE_DIR)
            conn.send("\n".join(files).encode())

        else:
            conn.send(b"ERROR: Unknown command")

def start_server(host="127.0.0.1", port=9001):
    os.makedirs(BASE_DIR, exist_ok=True)
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"Servidor escuchando en {host}:{port}")
    while True:
        conn, addr = s.accept()
        print(f"Conexion desde {addr}")
        handle_client(conn)
        conn.close()

if __name__ == "__main__":
    start_server()
    