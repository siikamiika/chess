"""A chess player"""
from chess.exceptions import NotYourPiece, IllegalMove

class Player(object):
    """The player"""
    def __init__(self, color):
        self.color = color
        self.game = None

    def move(self, old_position, new_position, promotion=None):
        """Check if the piece at `old_position` belongs to player and try to move it."""
        piece = self.game.board.grid[old_position].piece
        if piece is None:
            raise IllegalMove(f"There is no piece at {old_position}")
        elif piece.color == self.color:
            self.game.move(piece, new_position, promotion=promotion)
        else:
            raise NotYourPiece(f"The piece at {old_position} isn't owned by you")

    def resign(self):
        """Resign from the game."""
        self.game.resign(self.color)
