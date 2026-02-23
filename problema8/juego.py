import socket
import threading

HOST = "127.0.0.1"
PORT = 9090

def receive(sock):
    while True:
        try:
            msg = sock.recv(4096).decode()
            if not msg:
                break
            print(msg)
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        try:
            move = input("Ingresa posición (0-8): ")
            sock.sendall(move.encode())
        except:
            break

if _name_ == "_main_":
    main()