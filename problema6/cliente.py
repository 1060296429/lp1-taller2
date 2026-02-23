import socket
import threading

HOST = '127.0.0.1'
PORT = 9000


def recibir(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    threading.Thread(target=recibir, args=(cliente,), daemon=True).start()

    while True:
        mensaje = input()
        cliente.sendall((mensaje + "\n").encode())


if __name__ == "__main__":
    main()