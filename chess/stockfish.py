import subprocess

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