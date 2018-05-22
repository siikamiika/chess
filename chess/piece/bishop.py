"""Implementation for bishop"""
from . import Piece
from ..colors import COLOR
from ..helpers import algdelta
from ..exceptions import IllegalMove

class Bishop(Piece):
    """A bishop of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♗',
            COLOR.black: '♝',
        }[COLOR.black] # black as in fill entire symbol

    def move(self, position):
        """Try to legally move the bishop to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        # the bishop moves diagonally
        if abs(file_delta) == abs(rank_delta) > 0:
            captured = self._move_diagonal(position)
        else:
            raise IllegalMove((self.position, position))

        super().move(position)

        return captured
