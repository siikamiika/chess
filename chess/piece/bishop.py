"""Implementation for bishop"""
from chess.piece import Piece
from chess.colors import COLOR
from chess.helpers import algdelta
from chess.exceptions import IllegalMove

class Bishop(Piece):
    """A bishop of either color"""
    def __init__(self, color: COLOR) -> None:
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♗',
            COLOR.black: '♝',
        }[COLOR.black] # black as in fill entire symbol

    def move(self, position, promotion=None, commit=True, stop_recursion=False):
        """Try to legally move the bishop to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        # the bishop moves diagonally
        if abs(file_delta) == abs(rank_delta) > 0:
            captured = self._move_diagonal(position)
        else:
            raise IllegalMove((self.position, position))

        super().move(position, commit=commit, stop_recursion=stop_recursion)

        return captured
