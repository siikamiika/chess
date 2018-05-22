"""A chess player"""
from .exceptions import NotYourPiece

class Player(object):
    """The player"""
    def __init__(self, color):
        self.color = color
        self.game = None

    def move(self, old_position, new_position):
        """Check if the piece at `old_position` belongs to player and try to move it."""
        piece = self.game.board.grid[old_position].piece
        if piece.color == self.color:
            self.game.move(piece, new_position)
        else:
            raise NotYourPiece(f"The piece at {old_position} isn't owned by you")
