"""Implementation for queen"""
from . import Piece
from ..colors import COLOR
from ..helpers import algdelta
from ..exceptions import IllegalMove

class Queen(Piece):
    """A queen of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♕',
            COLOR.black: '♛',
        }[COLOR.black] # black as in fill entire symbol

    def move(self, position, commit=True):
        """Try to legally move the queen to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        if (    # the queen moves along a rank
                (abs(file_delta) > 0 and rank_delta == 0) or
                # the queen moves along a file
                (abs(rank_delta) > 0 and file_delta == 0)
            ):
            captured = self._move_parallel(position)
        # the queen moves diagonally
        elif abs(file_delta) == abs(rank_delta) > 0:
            captured = self._move_diagonal(position)
        else:
            raise IllegalMove((self.position, position))

        super().move(position, commit=commit)

        return captured
