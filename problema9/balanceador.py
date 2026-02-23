import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

BACKENDS = [9001, 9002, 9003]
alive_servers = []
current = 0


def health_check():
    global alive_servers

    while True:
        new_alive = []

        for port in BACKENDS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((HOST, port + 100))
                s.recv(16)
                new_alive.append(port)
                s.close()
            except:
                pass

        alive_servers = new_alive


def get_server():
    global current

    if not alive_servers:
        return None

    server = alive_servers[current % len(alive_servers)]
    current += 1
    return server


def handle_client(client_conn):
    server_port = get_server()

    if server_port is None:
        client_conn.sendall(b"No hay servidores disponibles")
        client_conn.close()
        return

    try:
        backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend.connect((HOST, server_port))

        data = client_conn.recv(4096)
        backend.sendall(data)

        response = backend.recv(4096)
        client_conn.sendall(response)

    except:
        client_conn.sendall(b"Error conectando backend")

    client_conn.close()


def main():
    lb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb.bind((HOST, PORT))
    lb.listen()

    print("Balanceador activo en puerto 8000")

    threading.Thread(target=health_check, daemon=True).start()

    while True:
        conn, _ = lb.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    main()