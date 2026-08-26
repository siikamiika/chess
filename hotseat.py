#!/usr/bin/env python3
"""Hot seat example"""
import argparse

from chess import Chess, Player
from chess.colors import COLOR
import os


def main():
    parser = argparse.ArgumentParser(description="Hot seat chess game.")
    parser.add_argument("--state_path", nargs="?", default=None, help="Path to the game state file")
    args = parser.parse_args()

    state_path = args.state_path

    if state_path and os.path.exists(state_path):
        game = Chess.from_file(state_path)
        player1 = game.players[COLOR.white]
        player2 = game.players[COLOR.black]
    else:
        game = Chess()
        player1 = Player(COLOR.white)
        player2 = Player(COLOR.black)
        game.add_player(player1)
        game.add_player(player2)
        game.start()

    while True:
        try:
            player = game.players[game.turn]
            print(game)
            move = input(f'{player.color.name} move: ')
            player.move(*Chess.parse_move(move))
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            input('Press return to continue...')
            continue

if __name__ == '__main__':
    main()
