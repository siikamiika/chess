"""The game of chess"""
from itertools import zip_longest
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
    GameAlreadyStarted,
    GameOver,
)
from .helpers import char_range, rpad_ansi, algdelta

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
        self.over = False

    def add_player(self, player):
        """Add players to a game that hasn't started yet."""
        if self.started:
            raise GameAlreadyStarted('The game has already started')
        if not self.players[player.color]:
            player.game = self
            self.players[player.color] = player
        else:
            raise PlayerExists(f'There is already a player of the color {player.color}')

    def start(self):
        """If both of the players are present, the game can start."""
        if not self.started and self.players[COLOR.white] and self.players[COLOR.black]:
            self.started = True
            self.turn = COLOR.white

    def move(self, piece, position):
        """Check if it's the piece's turn to move and try to move the piece on the chessboard."""
        if self.over:
            raise GameOver('The game is already over')
        if not self.started:
            raise GameNotStarted('You must start the game first')
        if not self.turn == piece.color:
            raise NotYourTurn("Wait for your turn")

        old_position = piece.position
        # try to move the piece
        captured = self.board.move(piece, position)
        # if a pawn reaches to the opposite edge, promote it
        if piece.promoted_piece:
            piece = piece.promoted_piece
            self.pieces[piece.piece_id] = piece
        if captured:
            # remove captured piece from chessboard and add it to captured pieces
            self.board[captured.position].piece = None
            captured.captured = True
            self.captured[captured.color].append(captured)
        # finally move the piece on the chessboard
        self.board[old_position].piece = None
        self.board[position].piece = piece
        # the move was successful, add it to the game moves
        self._log_move(old_position, position, piece, captured)
        # change turn
        self.turn = COLOR.white if self.turn == COLOR.black else COLOR.black
        return captured

    def _log_move(self, old_position, position, piece, captured):
        other_color = COLOR.black if piece.color == COLOR.white else COLOR.white
        threatening_pieces = self._is_check(other_color)
        mate = threatening_pieces and self._is_mate(other_color, threatening_pieces)
        stale = not threatening_pieces and not self._can_move(other_color)

        self.moves.append(dict(
            move_from=old_position,
            move_to=position,
            piece=piece,
            move_id=len(self.moves),
            captured=captured,
            check=bool(threatening_pieces),
            mate=mate,
            stale=stale,
        ))

        if mate:
            raise GameOver(f'Game over. {piece.color.name.capitalize()} wins')
        elif stale:
            raise GameOver('Game over. Stalemate')

    def results_in_check(self, piece, position):
        """Before letting the piece move be committed, check if it would result in check"""
        # backup
        original_position = piece.position
        target_piece = self.board[position].piece
        # fake commit
        if target_piece:
            target_piece.captured = True
        self.board[original_position].piece = None
        self.board[position].piece = piece
        piece.moves.append((original_position, position, len(self.moves)))
        piece.position = position
        # check check
        threatening_pieces = self._is_check(piece.color)
        # undo commit
        if target_piece:
            target_piece.captured = False
        self.board[position].piece = target_piece
        piece.moves.pop()
        piece.position = original_position
        self.board[original_position].piece = piece

        return bool(threatening_pieces)

    def _is_check(self, color):
        """If color's king is in check, return the threatening pieces"""
        pieces = [p for p in self.pieces.values() if not p.captured]
        king = next(p for p in pieces if isinstance(p, King) and p.color == color)
        threatening_pieces = []
        for piece in pieces:
            if piece.color != color:
                if piece.can_capture(king.position):
                    threatening_pieces.append(piece)
        return threatening_pieces

    def _is_mate(self, color, threatening_pieces):
        """color's opponent has won"""
        pieces = [p for p in self.pieces.values() if p.color == color and not p.captured]
        king = next(p for p in pieces if isinstance(p, King))
        if not king.can_move():
            # if the check can be prevented by capturing the threatening piece
            for threatening_piece in threatening_pieces:
                for piece in pieces:
                    if piece.can_capture(threatening_piece.position):
                        return False
            # if the check can be prevented by interposing a piece between the
            # threatening piece and the king
            for threatening_piece in [p for p in threatening_pieces
                                      if not isinstance(p, (Knight, Pawn))]:
                start, end = threatening_piece.position, king.position
                file_delta, rank_delta = algdelta(start, end)
                # diagonal
                if abs(file_delta) != abs(rank_delta):

                    intermediate_positions = zip(
                        char_range(start[0], end[0]),
                        char_range(start[1], end[1])
                    )
                    prev = next(intermediate_positions) # skip the starting position
                # parallel
                else:
                    intermediate_positions = zip_longest(
                        char_range(start[0], end[0]),
                        char_range(start[1], end[1]),
                        fillvalue=end[0 if start[0] == end[0] else 1]
                    )
                    prev = ''.join(next(intermediate_positions)) # skip the starting position
                # all squares between the threatening piece and the king
                positions = []
                for pos in intermediate_positions:
                    positions.append(prev)
                    prev = ''.join(pos)
                for position in positions:
                    # check if the attacker and the king can be interposed
                    for piece in pieces:
                        if piece.can_reach(position):
                            return False
            self.over = True
            return True

    def _can_move(self, color):
        """If color can't move but isn't in check, the game ends in stalemate"""
        pieces = [p for p in self.pieces.values() if p.color == color and not p.captured]
        for piece in pieces:
            if piece.can_move():
                return True

    def _generate_pieces(self):
        # black
        self.board['a8'].piece = Rook(COLOR.black)
        self.board['b8'].piece = Knight(COLOR.black)
        self.board['c8'].piece = Bishop(COLOR.black)
        self.board['d8'].piece = Queen(COLOR.black)
        self.board['e8'].piece = King(COLOR.black)
        self.board['f8'].piece = Bishop(COLOR.black)
        self.board['g8'].piece = Knight(COLOR.black)
        self.board['h8'].piece = Rook(COLOR.black)
        for file in char_range('a', 'h'):
            self.board[f'{file}7'].piece = Pawn(COLOR.black)

        # white
        for file in char_range('a', 'h'):
            self.board[f'{file}2'].piece = Pawn(COLOR.white)
        self.board['a1'].piece = Rook(COLOR.white)
        self.board['b1'].piece = Knight(COLOR.white)
        self.board['c1'].piece = Bishop(COLOR.white)
        self.board['d1'].piece = Queen(COLOR.white)
        self.board['e1'].piece = King(COLOR.white)
        self.board['f1'].piece = Bishop(COLOR.white)
        self.board['g1'].piece = Knight(COLOR.white)
        self.board['h1'].piece = Rook(COLOR.white)

        self.board.update_piece_positions()

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
