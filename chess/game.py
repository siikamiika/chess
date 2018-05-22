"""The game of chess"""
from .player import Player
from .board import Board
from .piece import (
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
)
from .colors import COLOR, BG2, RESET_STYLE, FG_WHITE, FG_BLACK
from .exceptions import PlayerExists
from .helpers import char_range, rpad_ansi

class Chess(object):
    """The game"""
    def __init__(self):
        self.board = Board(self)
        self.moves = []
        self.players = {
            COLOR.white: None,
            COLOR.black: None
        }
        self.pieces = {}
        self.captured = {
            COLOR.white: [],
            COLOR.black: []
        }
        self._generate_pieces()

    def add_player(self, player):
        if player.color not in self.players:
            self.players[player.color] = player
        else:
            raise PlayerExists

    def _generate_pieces(self):
        # black
        self.board.grid['a8'].piece = Rook(COLOR.black)
        self.board.grid['b8'].piece = Knight(COLOR.black)
        self.board.grid['c8'].piece = Bishop(COLOR.black)
        self.board.grid['d8'].piece = Queen(COLOR.black)
        self.board.grid['e8'].piece = King(COLOR.black)
        self.board.grid['f8'].piece = Bishop(COLOR.black)
        self.board.grid['g8'].piece = Knight(COLOR.black)
        self.board.grid['h8'].piece = Rook(COLOR.black)
        for file in char_range('a', 'h'):
            self.board.grid[f'{file}7'].piece = Pawn(COLOR.black)

        # white
        for file in char_range('a', 'h'):
            self.board.grid[f'{file}2'].piece = Pawn(COLOR.white)
        self.board.grid['a1'].piece = Rook(COLOR.white)
        self.board.grid['b1'].piece = Knight(COLOR.white)
        self.board.grid['c1'].piece = Bishop(COLOR.white)
        self.board.grid['d1'].piece = Queen(COLOR.white)
        self.board.grid['e1'].piece = King(COLOR.white)
        self.board.grid['f1'].piece = Bishop(COLOR.white)
        self.board.grid['g1'].piece = Knight(COLOR.white)
        self.board.grid['h1'].piece = Rook(COLOR.white)

        self.board.grid.update_piece_positions()

    def __str__(self):
        rows = []

        # pieces captured from white
        captured_row = [' ' * 3, BG2] + [' '] * 24 + [RESET_STYLE, ' ' * 3]
        for i, captured in enumerate(self.captured[COLOR.white]):
            captured_row[i + 2] = str(captured)
        rows.append(''.join(captured_row))

        # chessboard
        rows += str(self.board).splitlines()

        # pieces captured from black
        captured_row = [' ' * 3, BG2] + [' '] * 24 + [RESET_STYLE, ' ' * 3]
        for i, captured in enumerate(self.captured[COLOR.black]):
            captured_row[i + 2] = str(captured)
        rows.append(''.join(captured_row))

        # list of moves
        log = [[BG2, ' ' * 7, RESET_STYLE] for _ in range(len(rows))]
        for i, log_data in enumerate(self.moves[-len(rows):]):
            log_text = []

            if isinstance(log_data['piece'], Pawn):
                log_text.append(FG_WHITE if log_data['piece'].color == COLOR.white else FG_BLACK)
                if log_data['captured']:
                    log_text.append(log_data['move_from'][0] + 'x')
            else:
                log_text.append(str(log_data['piece']))
                if log_data['captured']:
                    log_text.append('x')

            log_text.append(log_data['move_to'])

            log[i][1] = rpad_ansi(''.join(log_text), 7, ' ')

        # chessboard and captured pieces on the left, list of moves on the right
        log_rows = [''.join(l) for l in log]
        combined = zip(rows, log_rows)
        return '\n'.join(r + l for r, l in combined)
