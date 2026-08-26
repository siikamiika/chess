"""Implementation for rook"""
from chess.piece import Piece
from chess.colors import COLOR
from chess.helpers import algdelta
from chess.exceptions import IllegalMove

class Rook(Piece):
    """A rook of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♖',
            COLOR.black: '♜',
        }[COLOR.black] # black as in fill entire symbol

    def move(self, position, promotion=None, commit=True, stop_recursion=False):
        """Try to legally move the rook to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        if (    # the rook moves along a rank
                (abs(file_delta) > 0 and rank_delta == 0) or
                # the rook moves along a file
                (abs(rank_delta) > 0 and file_delta == 0)
            ):
            captured = self._move_parallel(position)
        else:
            raise IllegalMove((self.position, position))

        super().move(position, commit=commit, stop_recursion=stop_recursion)

        return captured
