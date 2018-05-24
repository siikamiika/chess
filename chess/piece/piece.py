"""The black and white pieces used in the game"""
from itertools import zip_longest
from ..colors import FG_WHITE, FG_BLACK, COLOR
from ..helpers import is_position, char_range
from ..exceptions import IllegalMove

class Piece(object):
    """A base piece"""
    def __init__(self, color):
        self.color = color
        self.piece_id = -1
        self.position = '' # init from Grid.update_piece_positions
        self.game = None   # init from Grid.update_piece_positions
        self.symbol = ' '
        self.moves = []
        self.captured = False
        self.promoted_piece = None # pawn only

    def move(self, position, commit=True):
        """Move the piece to the target position."""
        if self.game.results_in_check(self, position):
            raise IllegalMove("You can't put your king in check")
        if commit:
            move = (self.position, position, len(self.game.moves))
            self.moves.append(move)
            self.position = position

    def can_reach(self, position):
        """If the piece can reach position, return True"""
        try:
            self.move(position, commit=False)
            return True
        except IllegalMove:
            return False

    def can_capture(self, position):
        """If the piece can capture a piece at position, return True"""
        return self.can_reach(position)

    def can_move(self):
        """Check if the piece can move at all"""
        positions = [f + r for r in char_range('1', '8') for f in char_range('a', 'h')]
        return any(self.can_reach(p) for p in positions)

    def get_starting_position(self):
        """Get the square where this piece started from."""
        if not self.moves:
            if is_position(self.position):
                return self.position
            else:
                raise ValueError(f'{self.position} is not a valid position')
        else:
            return self.moves[0][0]


    def _move_parallel(self, position):
        """Move the piece along a file or a rank"""
        captured = None

        intermediate_positions = zip_longest(
            char_range(self.position[0], position[0]),
            char_range(self.position[1], position[1]),
            fillvalue=position[0 if self.position[0] == position[0] else 1]
        )
        next(intermediate_positions) # skip the starting position

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

        return captured

    def _move_diagonal(self, position):
        """Move the piece diagonally"""
        captured = None

        intermediate_positions = zip(
            char_range(self.position[0], position[0]),
            char_range(self.position[1], position[1])
        )
        next(intermediate_positions) # skip the starting position

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

        return captured

    def __str__(self):
        fgcolor = FG_WHITE if self.color == COLOR.white else FG_BLACK
        return f'{fgcolor}{self.symbol}'

    def __repr__(self):
        return f'<{self.color.name.capitalize()} {self.__class__.__name__}>'
