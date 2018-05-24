#!/usr/bin/env python3
"""Testing"""
import time
from chess import Chess, Player
from chess.exceptions import IllegalMove
from chess.piece import Queen
from chess.colors import COLOR

def move(piece, position, capture=False, must_fail=False):
    captured = None
    try:
        piece.game.turn = piece.color # force turn
        captured = piece.game.move(piece, position)
        if must_fail:
            assert False
    except IllegalMove as ex:
        if not must_fail:
            raise ex
    if capture:
        assert captured
    else:
        assert not captured
    print(piece.game)
    # time.sleep(1)

def test_check(game):
    king = game.board['e1'].piece
    game.board['e2'].piece = None
    move(king, 'e2')
    move(king, 'e3')
    move(king, 'e4')
    move(king, 'e5')
    move(king, 'e6')
    move(king, 'e7')
    move(king, 'e8')


def main():
    game = Chess()
    player1 = Player(COLOR.white)
    player2 = Player(COLOR.black)
    game.add_player(player1)
    game.add_player(player2)
    game.start()

    test_check(game)

if __name__ == '__main__':
    main()
