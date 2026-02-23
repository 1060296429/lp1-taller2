import socket
import threading
import json
import time

HOST = "127.0.0.1"
PORT = int(input("Puerto del backend: "))

clientes_data = {}
other_servers = [9001, 9002, 9003]  # puertos posibles


def replicate_data():
    """Replica los datos a otros servidores"""
    while True:
        time.sleep(5)
        for port in other_servers:
            if port == PORT:
                continue
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, port))
                s.sendall(("SYNC " + json.dumps(clientes_data)).encode())
                s.close()
            except:
                pass


def handle_client(conn, addr):
    global clientes_data

    try:
        data = conn.recv(4096).decode()

        if data.startswith("SYNC"):
            json_data = data[5:]
            clientes_data.update(json.loads(json_data))
            conn.close()
            return

        print("Cliente conectado:", addr)

        mensaje = f"Servidor {PORT} te atendió"
        conn.sendall(mensaje.encode())

        # guardar cliente (simulación de base de datos)
        clientes_data[str(addr)] = time.ctime()

    except:
        pass

    conn.close()


def health_server():
    """Responde a health checks"""
    health = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    health.bind((HOST, PORT + 100))
    health.listen()

    while True:
        conn, _ = health.accept()
        conn.sendall(b"OK")
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Backend activo en puerto {PORT}")

    threading.Thread(target=replicate_data, daemon=True).start()
    threading.Thread(target=health_server, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()