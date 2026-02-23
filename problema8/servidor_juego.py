import socket
import threading

HOST = "0.0.0.0"
PORT = 9090

board = [" "] * 9
players = []
spectators = []
turn = 0
game_active = True

lock = threading.Lock()


def print_board():
    return f"""
 {board[0]} | {board[1]} | {board[2]}
---+---+---
 {board[3]} | {board[4]} | {board[5]}
---+---+---
 {board[6]} | {board[7]} | {board[8]}
"""


def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "Empate"
    return None


def broadcast(msg):
    for conn in players + spectators:
        try:
            conn.sendall(msg.encode())
        except:
            pass


def handle_client(conn, addr):
    global turn, game_active

    print("Conectado:", addr)

    with lock:
        if len(players) < 2:
            players.append(conn)
            symbol = "X" if len(players) == 1 else "O"
            conn.sendall(f"Eres jugador {symbol}\n".encode())
        else:
            spectators.append(conn)
            conn.sendall("Eres espectador\n".encode())
            conn.sendall(print_board().encode())

    while game_active:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            if conn in players:
                idx = players.index(conn)

                if idx != turn:
                    conn.sendall("No es tu turno\n".encode())
                    continue

                if not data.isdigit():
                    continue

                move = int(data)

                with lock:
                    if move < 0 or move > 8 or board[move] != " ":
                        conn.sendall("Movimiento inválido\n".encode())
                        continue

                    symbol = "X" if idx == 0 else "O"
                    board[move] = symbol

                    broadcast(print_board())

                    winner = check_winner()
                    if winner:
                        broadcast(f"Fin del juego: {winner}\n")
                        game_active = False
                        break

                    turn = 1 - turn
                    players[turn].sendall("Tu turno\n".encode())

        except:
            break

    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor de juego activo en puerto {PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()