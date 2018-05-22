"""Implementation for knight"""
from . import Piece
from ..colors import COLOR
from ..helpers import algdelta
from ..exceptions import IllegalMove

class Knight(Piece):
    """A knight of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♘',
            COLOR.black: '♞',
        }[COLOR.black] # black as in fill entire symbol

    def move(self, position):
        """Try to legally move the knight to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        if (    # the knight moves 2 horizontally, then 1 vertically
                abs(file_delta) == 2 and abs(rank_delta) == 1 or
                # the knight moves 2 vertically, then 1 horizontally
                abs(rank_delta) == 2 and abs(file_delta) == 1
            ):
            square = self.game.board[position]
            if square.piece:
                if square.piece.color != self.color:
                    captured = square.piece
                else: # your own piece is in the way
                    raise IllegalMove(f'There is a piece at {position}')
        else:
            raise IllegalMove((self.position, position))

        super().move(position)

        return captured
