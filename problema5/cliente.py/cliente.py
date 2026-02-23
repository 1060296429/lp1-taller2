import socket
import os
import hashlib

HOST = 'localhost'
PORT = 9001
BUFFER_SIZE = 4096


mport socket
def upload_file(filename, host="127.0.0.1", port=6000):
    s = socket.socket()
    s.connect((host, port))
    s.send(f"UPLOAD {filename}".encode())
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(BUFFER_SIZE), b""):
            s.send(chunk)
    s.send(b"EOF")
    print("Checksum recibido:", s.recv(1024).decode())
    s.close()

def download_file(filename, host="127.0.0.1", port=6000):
    s = socket.socket()
    s.connect((host, port))
    s.send(f"DOWNLOAD {filename}".encode())
    with open("downloaded_" + filename, "wb") as f:
        while True:
            data = s.recv(BUFFER_SIZE)
            if data == b"EOF":
                break
            f.write(data)
    print("Checksum recibido:", s.recv(1024).decode())
    s.close()

def list_files(host="127.0.0.1", port=6000):
    s = socket.socket()
    s.connect((host, port))
    s.send(b"LIST")
    print("Archivos en servidor:\n", s.recv(4096).decode())
    s.close()