import time
import argparse

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import GameOver


def main():
    parser = argparse.ArgumentParser(description="Replay a chess game from a saved state")
    parser.add_argument("--state_path", nargs=None, default=None, help="Path to the game state file")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between moves in seconds")
    args = parser.parse_args()

    state_path = args.state_path
    delay = args.delay

    with open(state_path) as f:
        moves = f.read().splitlines()

    game = Chess()

    player1 = Player(COLOR.white)
    player2 = Player(COLOR.black)

    game.add_player(player1)
    game.add_player(player2)

    game.start()

    for move in moves:
        time.sleep(delay)
        try:
            player = game.players[game.turn]
            print(game)
            player.move(*Chess.parse_move(move))
        except GameOver as e:
            print(game)
            print(f'{e.__class__.__name__}: {e}')
            break
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            break


if __name__ == '__main__':
    main()
