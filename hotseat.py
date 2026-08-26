#!/usr/bin/env python3
"""Hot seat example"""
from chess import Chess, Player
from chess.colors import COLOR
import os

def main():
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
            player.move(*input(f'{player.color.name} move: ').split())
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            input('Press return to continue...')
            continue

if __name__ == '__main__':
    main()
