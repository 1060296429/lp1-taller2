import socket

HOST = "127.0.0.1"
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.sendall(b"Hola servidor")

respuesta = client.recv(4096)
print("Respuesta:", respuesta.decode())

client.close()