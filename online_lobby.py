import socket
import argparse
import threading

from chess import Chess, Player
from chess.exceptions import GameOver
from chess.colors import COLOR


HOST = '0.0.0.0'
PORT = 42069


class OnlinePlayer:
    def __init__(self, player, player_type, password, online_game):
        self.player_type = player_type
        self.player = player
        self.password = password
        self.online_game = online_game

    def move(self, move):
        try:
            with self.online_game.move_lock:
                self.player.move(*Chess.parse_move(move))
                self.online_game.broadcast_state()
        except GameOver as e:
            print(f"Game over: {e}")
            self.online_game.broadcast_state()
        except Exception as e:
            print(f"Error making move: {e}")


class OnlineGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.game = Chess()
        self.players = {
            COLOR.white: None,
            COLOR.black: None,
        }
        self.connections = []
        self.move_lock = threading.Lock()

    def add_player(self, color, player_type, password):
        player = Player(color)
        self.game.add_player(player)
        if color == COLOR.white:
            self.players[COLOR.white] = OnlinePlayer(player, player_type, password, self)
            return self.players[COLOR.white]
        elif color == COLOR.black:
            self.players[COLOR.black] = OnlinePlayer(player, player_type, password, self)
            return self.players[COLOR.black]

    def start_game(self):
        self.game.start()
        self.broadcast_state()

    def get_state(self):
        out = [str(self.game)]
        if self.game.over:
            if self.game.winner:
                out.append(f'Game over. Winner: {self.game.winner.name}')
            else:
                out.append('Game over. Stalemate.')
        elif self.game.turn:
            player = self.game.players[self.game.turn]
            out.append(f'{player.color.name} move: ')
        return '\n'.join(out)

    def broadcast_state(self):
        for conn in self.connections:
            try:
                conn.sendall((self.get_state()).encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to a connection: {e}")


class OnlineLobby:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.games = {}
        self.server_socket = None
        self.add_game_lock = threading.Lock()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        thread = threading.Thread(target=self._background_accept, daemon=True)
        thread.start()
        return thread

    def handle_client(self, conn, addr):
        print(f"Handling client {addr}")
        try:
            online_game = self._handle_join_game(conn)
            online_game.connections.append(conn)
            player = self._handle_color_choice(conn, online_game)
            self._handle_client_loop(conn, player)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            conn.close()
            print(f"Connection with {addr} closed")

    def _handle_join_game(self, conn):
        while True:
            payload = []
            for game_id in self.games:
                payload.append(str(game_id))
            payload.append("Enter game ID or 'new' for a new game: ")
            conn.sendall("\n".join(payload).encode('utf-8'))
            data = conn.recv(1024)
            if not data:
                break
            choice = data.decode().strip()
            if choice == "new":
                with self.add_game_lock:
                    online_game = self._create_game()
                    self.games[online_game.game_id] = online_game
                conn.sendall(f"Created new game with ID {online_game.game_id}\n".encode('utf-8'))
                return online_game
            elif choice.isdigit() and int(choice) in self.games:
                online_game = self.games[int(choice)]
                conn.sendall(f"Joined game with ID {online_game.game_id}\n".encode('utf-8'))
                return online_game
            else:
                conn.sendall("Invalid choice. Try again.\n".encode('utf-8'))
                continue

    def _handle_color_choice(self, conn, online_game):
        while True:
            conn.sendall(f"Choose color (white/black): ".encode('utf-8'))
            color_data = conn.recv(1024)
            if not color_data:
                break
            color_choice = color_data.decode('utf-8').strip().lower()
            if color_choice in ["white", "black"]:
                color = COLOR.white if color_choice == "white" else COLOR.black
                if online_game.players[color] is None:
                    conn.sendall("Enter password: \n".encode('utf-8'))
                    password_data = conn.recv(1024)
                    if not password_data:
                        break
                    password = password_data.decode('utf-8').strip()
                    player = online_game.add_player(color, "human", password)
                    if online_game.game.players[COLOR.white] is not None and online_game.game.players[COLOR.black] is not None:
                        online_game.start_game()
                    return player
                else:
                    conn.sendall(f"{color_choice.capitalize()} player already exists. Enter password: \n".encode('utf-8'))
                    password_data = conn.recv(1024)
                    if not password_data:
                        break
                    password = password_data.decode('utf-8').strip()
                    if online_game.players[color].password != password:
                        conn.sendall("Incorrect password. Try again.\n".encode('utf-8'))
                        continue
                    conn.sendall(online_game.get_state().encode('utf-8'))
                    return online_game.players[color]
            else:
                conn.sendall("Invalid color choice. Try again.\n".encode('utf-8'))
                continue

    def _handle_client_loop(self, conn, player):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            player.move(data.decode('utf-8').strip())

    def accept_connection(self):
        conn, addr = self.server_socket.accept()
        print(f"Connected by {addr}")
        return conn, addr

    def _create_game(self):
        online_game = OnlineGame(len(self.games) + 1)
        return online_game

    def _background_accept(self):
        while True:
            conn, addr = self.accept_connection()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()


def main():
    parser = argparse.ArgumentParser(description="Play against other players in an online lobby.")
    parser.add_argument("--host", nargs="?", default=HOST, help="Host to bind the server to")
    parser.add_argument("--port", nargs="?", type=int, default=PORT, help="Port to bind the server to")
    args = parser.parse_args()

    lobby = OnlineLobby(host=args.host, port=args.port)
    server = lobby.start_server()
    server.join()

if __name__ == "__main__":
    main()
