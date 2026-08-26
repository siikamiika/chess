import subprocess
import random
import sys
import time

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import GameOver


class Stockfish:
    def __init__(self, binary_path):
        self.process = subprocess.Popen(
            binary_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Initialize the engine using the UCI protocol
        self._send_command("uci")
        self._wait_for("uciok")
        self._send_command("isready")
        self._wait_for("readyok")

    def _send_command(self, command):
        self.process.stdin.write(f"{command}\n")
        self.process.stdin.flush()

    def _wait_for(self, target_string):
        while True:
            line = self.process.stdout.readline().strip()
            if not line:
                continue
            if target_string in line:
                return line

    def set_position(self, moves=None):
        """Sets the board position. 'moves' is a list of UCI moves (e.g., ['e2e4', 'e7e5'])."""
        if moves:
            moves_str = " ".join(moves)
            self._send_command(f"position startpos moves {moves_str}")
        else:
            self._send_command("position startpos")

    def get_best_move(self, time_ms=1000):
        """Asks the engine to calculate the best move for a given time (in milliseconds)."""
        self._send_command(f"go movetime {time_ms}")

        # The engine will output various calculation lines, 
        # but always ends its turn with a line starting with 'bestmove'
        best_move_line = self._wait_for("bestmove")

        # Format: "bestmove e2e4 ponder e7e5"
        print(best_move_line)  # Debugging output
        return best_move_line.split()[1]

    def close(self):
        """Safely shuts down the engine process."""
        self._send_command("quit")
        self.process.terminate()


def main():
    stockfish_path = sys.argv[1] if len(sys.argv) > 1 else "stockfish"
    state_path = sys.argv[2] if len(sys.argv) > 2 else None

    moves = []
    if state_path:
        game = Chess.from_file(state_path)
        moves = list(map(lambda m: m['move_from'] + m['move_to'] + (m['promotion'] if m['promotion'] else ''), game.moves))

        player1 = game.players[COLOR.white]
        player2 = game.players[COLOR.black]

    else:
        game = Chess()

        player1 = Player(COLOR.white)
        player2 = Player(COLOR.black)

        game.add_player(player1)
        game.add_player(player2)

        game.log_moves_to_file(f'stockfish_moves_{int(time.time())}.txt')

        game.start()

        player1.game.turn = player1.color

    engine = Stockfish(stockfish_path)
    engine.set_position(moves)


    players = [player1, player2]

    turn = len(moves) % 2 == 1
    while True:
        try:
            player = players[turn]
            print(player.game)
            move = engine.get_best_move(time_ms=random.randint(100, 500))
            player.move(*Chess.parse_move(move))
            moves.append(move)
            engine.set_position(moves)
            turn = not turn
        except GameOver as e:
            print(f'{e.__class__.__name__}: {e}')
            break
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            input('Press return to continue...')
            continue


    engine.close()

if __name__ == '__main__':
    main()
