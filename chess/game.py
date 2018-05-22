"""The game of chess"""
from .board import Board
from .piece import (
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
)
from .colors import (
    COLOR,
    BG2,
    RESET_STYLE,
    FG_WHITE,
    FG_BLACK
)
from .exceptions import (
    PlayerExists,
    NotYourTurn,
    GameNotStarted,
    GameAlreadyStarted
)
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
        # state
        self.started = False
        self.turn = None

    def add_player(self, player):
        """Add players to a game that hasn't started yet."""
        if self.started:
            raise GameAlreadyStarted
        if not self.players[player.color]:
            player.game = self
            self.players[player.color] = player
        else:
            raise PlayerExists

    def start(self):
        """If both of the players are present, the game can start."""
        if not self.started and self.players[COLOR.white] and self.players[COLOR.black]:
            self.started = True
            self.turn = COLOR.white

    def move(self, piece, position):
        """Check if it's the piece's turn to move and try to move the piece on the chessboard."""
        if not self.started:
            raise GameNotStarted
        if not self.turn == piece.color:
            raise NotYourTurn

        old_position = piece.position
        # try to move the piece
        captured = self.board.move(piece, position)
        # if a pawn reaches to the opposite edge, promote it
        if piece.promoted_piece:
            piece = piece.promoted_piece
            self.pieces[piece.piece_id] = piece
        if captured:
            # remove captured piece from chessboard and add it to captured pieces
            self.board.grid[captured.position].piece = None
            self.captured[captured.color].append(captured)
        # finally move the piece on the chessboard
        self.board.grid[old_position].piece = None
        self.board.grid[position].piece = piece
        # the move was successful, add it to the game moves
        self._log_move(old_position, position, piece, captured)
        # change turn
        self.turn = COLOR.white if self.turn == COLOR.black else COLOR.black
        return captured

    def _log_move(self, old_position, position, piece, captured):
        self.moves.append(dict(
            move_from=old_position,
            move_to=position,
            piece=piece,
            move_id=len(self.moves),
            captured=captured,
            check=False, # TODO
            mate=False, # TODO
        ))

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
