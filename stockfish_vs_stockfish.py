import random
import sys
import time
import argparse

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import GameOver
from chess.stockfish import Stockfish


def main():
    parser = argparse.ArgumentParser(description="Stockfish vs Stockfish with short and random move times. Useful for testing")
    parser.add_argument("--stockfish_path", nargs="?", default="stockfish", help="Path to the Stockfish binary")
    parser.add_argument("--state_path", nargs="?", default=None, help="Path to the game state file")
    args = parser.parse_args()

    stockfish_path = args.stockfish_path
    state_path = args.state_path

    moves = []
    if state_path:
        game = Chess.from_file(state_path)
        moves = list(map(lambda m: m['move_from'] + m['move_to'] + (m['promotion'] if m['promotion'] else ''), game.moves))
    else:
        game = Chess()

        player1 = Player(COLOR.white)
        player2 = Player(COLOR.black)

        game.add_player(player1)
        game.add_player(player2)

        game.log_moves_to_file(f'stockfish_moves_{int(time.time())}.txt')

        game.start()

    engine = Stockfish(stockfish_path)
    engine.set_position(moves)

    while True:
        try:
            player = game.players[game.turn]
            print(game)
            move = engine.get_best_move(time_ms=random.randint(100, 500))
            player.move(*Chess.parse_move(move))
            moves.append(move)
            engine.set_position(moves)
        except GameOver as e:
            print(game)
            print(f'{e.__class__.__name__}: {e}')
            break
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            break


    engine.close()

if __name__ == '__main__':
    main()
