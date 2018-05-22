#!/usr/bin/env python3
"""Testing"""
import time
from chess import Chess
from chess.exceptions import IllegalMove
from chess.piece import Queen

def move(piece, position, capture=False, must_fail=False):
    captured = None
    try:
        captured = piece.game.board.move(piece, position)
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
    time.sleep(1)

def test_pawn(game):
    white_test_pawn = game.board.grid['a2'].piece
    black_test_pawn = game.board.grid['b7'].piece

    move(white_test_pawn, 'a4') # move 2 forward
    move(white_test_pawn, 'a4', must_fail=True) # move 2 forward again
    move(white_test_pawn, 'a5')
    move(white_test_pawn, 'a4', must_fail=True) # move backwards
    move(white_test_pawn, 'b6', must_fail=True) # capture nothing
    move(white_test_pawn, 'b5', must_fail=True) # move along a rank
    move(white_test_pawn, '`5', must_fail=True) # move out of bounds
    move(black_test_pawn, 'b5') # move next to white pawn
    move(white_test_pawn, 'b6', capture=True) # capture black pawn en passant

    print(white_test_pawn.moves)
    print(black_test_pawn.moves)
    print(game.moves)

    black_test_knight = game.board.grid['b8'].piece
    move(black_test_knight, 'c6')
    print(black_test_knight.moves)
    print(game.moves)

    move(white_test_pawn, 'b7')
    # promote the pawn to a queen
    move(white_test_pawn, 'b8')
    piece_id = white_test_pawn.piece_id
    assert isinstance(game.pieces[piece_id], Queen)

def test_rook(game):
    white_test_rook = game.board.grid['a1'].piece
    move(white_test_rook, 'a3')
    move(white_test_rook, 'b4', must_fail=True) # move diagonally
    move(white_test_rook, 'a7', capture=True)
    move(white_test_rook, 'b7')

def test_bishop(game):
    white_test_bishop = game.board.grid['c1'].piece
    move(white_test_bishop, 'a3', must_fail=True) # move when there is a piece in the way
    game.board.grid['b2'].piece = None # take the pawn out of the way
    print(game)
    move(white_test_bishop, 'a3')
    move(white_test_bishop, 'a3', must_fail=True) # don't move the bishop
    move(white_test_bishop, 'c3', must_fail=True) # move the bishop along rank 3
    move(white_test_bishop, 'd6')
    move(white_test_bishop, 'c7', capture=True)

def test_queen(game):
    white_test_queen = game.board.grid['d1'].piece
    move(white_test_queen, 'd2', must_fail=True) # move when there is a piece in the way
    move(white_test_queen, 'c1')
    move(white_test_queen, 'a3')
    move(white_test_queen, 'a4')
    move(white_test_queen, 'c5', must_fail=True) # move the queen like a knight
    move(white_test_queen, 'd7', must_fail=True) # capture a piece behind another piece
    move(white_test_queen, 'c6', capture=True)

def test_king(game):
    white_test_king = game.board.grid['e1'].piece
    move(white_test_king, 'd2', must_fail=True) # move when there is a piece in the way
    move(white_test_king, 'd1')
    move(white_test_king, 'c1')
    move(white_test_king, 'a3', must_fail=True) # move the king more than 1 at a time
    move(white_test_king, 'b2')
    move(white_test_king, 'c3')
    move(white_test_king, 'd4')
    move(white_test_king, 'd5')
    move(white_test_king, 'd6')
    move(white_test_king, 'd7', capture=True)
    move(white_test_king, 'd8', capture=True)
    move(white_test_king, 'd9', must_fail=True) # move out of bounds

def test_knight(game):
    white_test_knight = game.board.grid['b1'].piece
    move(white_test_knight, 'b3', must_fail=True) # move the knight 2 forward only
    move(white_test_knight, 'c3')
    move(white_test_knight, 'd5')
    move(white_test_knight, 'e7', capture=True)
    move(white_test_knight, 'g8', capture=True)
    move(white_test_knight, 'e9', must_fail=True) # move the knight out of bounds

def test_promoted_queen(game):
    white_test_queen = game.board.grid['b8'].piece
    move(white_test_queen, 'a7')
    move(white_test_queen, 'b5', must_fail=True) # move the promoted queen like a knight
    move(white_test_queen, 'c5')
    move(white_test_queen, 'd5')
    move(white_test_queen, 'f7', capture=True)
    move(white_test_queen, 'f8', capture=True)

def main():
    game = Chess()
    test_pawn(game)
    test_rook(game)
    test_bishop(game)
    test_queen(game)
    test_king(game)
    test_knight(game)
    test_promoted_queen(game)

if __name__ == '__main__':
    main()
