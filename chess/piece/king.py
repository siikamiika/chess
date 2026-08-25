"""Implementation for king"""
from itertools import zip_longest

from . import Piece
from ..colors import COLOR
from ..helpers import algdelta
from ..exceptions import IllegalMove
from .rook import Rook
from ..helpers import char_range

class King(Piece):
    """A king of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♔',
            COLOR.black: '♚',
        }[COLOR.black] # black as in fill entire symbol

    def _find_rook(self, position):
        """Find the rook that is involved in castling with this king"""
        file_delta, rank_delta = algdelta(self.position, position)
        if rank_delta != 0:
            raise IllegalMove((self.position, position))
        if file_delta > 0:
            rook_position = f'h{self.position[1]}'
        else:
            rook_position = f'a{self.position[1]}'
        rook = self.game.board[rook_position].piece
        return rook

    def _castle(self, position, commit=True):
        """Move the king and rook to their castling positions"""
        # basic checks
        if len(self.moves) > 0:
            raise IllegalMove((self.position, position))
        rook = self._find_rook(position)
        if not isinstance(rook, Rook) or rook.color != self.color or len(rook.moves) > 0:
            raise IllegalMove((self.position, position))

        # king
        file_delta, rank_delta = algdelta(self.position, position)
        if rank_delta != 0:
            raise IllegalMove((self.position, position))
        intermediate_positions = zip_longest(
            char_range(self.position[0], position[0]),
            char_range(self.position[1], position[1]),
            fillvalue=position[0 if self.position[0] == position[0] else 1]
        )
        next(intermediate_positions) # skip the starting position
        intermediate_positions = list(intermediate_positions)

        captured = None
        for file, rank in intermediate_positions:
            if captured: # a piece would have been captured on the previous iteration
                raise IllegalMove(f'There is a piece at {captured.position}')
            intermediate_pos = file + rank
            if self.game.results_in_check(self, intermediate_pos):
                raise IllegalMove(f'King would be in check at {intermediate_pos}')
            square = self.game.board[intermediate_pos]
            if square.piece:
                if square.piece.color != self.color:
                    captured = square.piece
                else: # your own piece is in the way
                    raise IllegalMove(f'There is a piece at {intermediate_pos}')

        # rook
        target_square = ''.join(intermediate_positions[-2])
        file_delta, rank_delta = algdelta(self.position, target_square)
        if rank_delta != 0:
            raise IllegalMove((self.position, position))
        intermediate_positions = zip_longest(
            char_range(self.position[0], position[0]),
            char_range(self.position[1], position[1]),
            fillvalue=position[0 if self.position[0] == position[0] else 1]
        )
        next(intermediate_positions) # skip the starting position
        intermediate_positions = list(intermediate_positions)

        for file, rank in intermediate_positions:
            if captured: # a piece would have been captured on the previous iteration
                raise IllegalMove(f'There is a piece at {captured.position}')
            intermediate_pos = file + rank
            square = self.game.board[intermediate_pos]
            if square.piece:
                if square.piece.color != self.color:
                    captured = square.piece
                else: # your own piece is in the way
                    raise IllegalMove(f'There is a piece at {intermediate_pos}')

        # update rook position on the board manually
        if commit:
            old_position = rook.position
            rook.move(target_square, commit=commit)
            self.game.board[old_position].piece = None
            self.game.board[target_square].piece = rook

        return captured

    def move(self, position, commit=True):
        """Try to legally move the king to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        if (    # the king moves along a rank
                (abs(file_delta) == 1 and rank_delta == 0) or
                # the king moves along a file
                (abs(rank_delta) == 1 and file_delta == 0)
            ):
            captured = self._move_parallel(position)
        # the king moves diagonally
        elif abs(file_delta) == abs(rank_delta) == 1:
            captured = self._move_diagonal(position)
        # the king moves two squares along a rank (castling)
        elif abs(file_delta) == 2 and rank_delta == 0:
            captured = self._castle(position, commit=commit)
            if captured:
                raise IllegalMove((self.position, position))
        else:
            raise IllegalMove((self.position, position))

        super().move(position, commit=commit)

        return captured
