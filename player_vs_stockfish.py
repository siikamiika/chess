import time
import argparse

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import GameOver
from chess.stockfish import Stockfish


def main():
    parser = argparse.ArgumentParser(description="Play against Stockfish.")
    parser.add_argument("--stockfish_path", nargs="?", default="stockfish", help="Path to the Stockfish binary")
    parser.add_argument("--state_path", nargs="?", default=None, help="Path to the game state file")
    parser.add_argument("--player_color", nargs="?", default="white", choices=["white", "black"], help="Color of the human player")
    parser.add_argument("--time_ms", nargs="?", type=int, default=1000, help="Time in milliseconds for Stockfish to think")
    args = parser.parse_args()

    stockfish_path = args.stockfish_path
    state_path = args.state_path
    player_color = COLOR.white if args.player_color == "white" else COLOR.black
    time_ms = args.time_ms

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
            if player.color == player_color:
                move = input("Your move: ")
            else:
                move = engine.get_best_move(time_ms=time_ms)
            player.move(*Chess.parse_move(move))
            moves.append(move)
            engine.set_position(moves)
        except GameOver as e:
            print(game)
            print(f'{e.__class__.__name__}: {e}')
            break
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            input('Press return to continue...')
            continue


    engine.close()

if __name__ == '__main__':
    main()
