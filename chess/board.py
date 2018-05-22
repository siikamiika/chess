"""A board where the game of chess is played"""
from itertools import chain
from .colors import BG1, BG2, RESET_STYLE
from .helpers import alg2grid, grid2alg, char_range, is_position
from .exceptions import IllegalMove

class Board(object):
    """The chessboard"""
    def __init__(self, game):
        self.game = game
        self.grid = Grid(game)

    def move(self, piece, position):
        """Check if the move is valid and move a piece to a position. If the
        position was already occupied by the opponent, return the captured piece."""
        if not is_position(position):
            raise IllegalMove(f"'{position}' doesn't look like a valid position")
        target_square = self[position]
        if target_square.piece and target_square.piece.color == piece.color:
            raise IllegalMove(f"{position} is already occupied by you")

        captured = piece.move(position)
        return captured

    def update_piece_positions(self):
        """Called in game init after the pieces are placed"""
        self.grid.update_piece_positions()

    def __str__(self):
        files_text = [f' {c} ' for c in chain(' ', char_range('a', 'h'), ' ')]
        files_text = ''.join(files_text)
        output_rows = [files_text]
        for rank in char_range('8', '1'):
            row = [f' {rank} ']
            for file in char_range('a', 'h'):
                square = self[f'{file}{rank}']
                row.append(f'{square}{RESET_STYLE}')
            row.append(f' {rank} ')
            output_rows.append(row)
        output_rows.append(files_text)

        return '\n'.join([''.join(r) for r in output_rows])

    def __getitem__(self, position):
        return self.grid[position]

    def __setitem__(self, position, item):
        self.grid[position] = item

    def __repr__(self):
        return f'<Board: {self.grid.squares}>'


class Square(object):
    """A chessboard square"""
    def __init__(self, rank, file):
        self.rank = rank
        self.file = file
        self.piece = None

    def __str__(self):
        bgcolor = BG1 if self.rank % 2 == self.file % 2 else BG2
        return f'{bgcolor} {self.piece or " "} '

    def __repr__(self):
        return f'<Square ({self.rank}, {self.file}): {self.piece}>'

class Grid(object):
    """An 8x8 grid containing the chessboard squares"""
    def __init__(self, game):
        self.game = game
        # (0, 0) is a8
        self.squares = [[Square(x, y) for x in range(8)] for y in range(8)]

    def update_piece_positions(self):
        """Give pieces ID's, a reference to the game instance (and vice versa) and
        let them know where they are positioned."""
        piece_id = 0
        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                if square.piece:
                    square.piece.game = self.game
                    square.piece.position = ''.join(grid2alg(j, i))
                    square.piece.piece_id = piece_id
                    self.game.pieces[piece_id] = square.piece
                    piece_id += 1

    def __getitem__(self, position):
        if not is_position(position):
            raise KeyError(position)
        grid_x, grid_y = alg2grid(position) # pylint: disable=unbalanced-tuple-unpacking
        return self.squares[grid_y][grid_x]

    def __setitem__(self, position, item):
        if not is_position(position):
            raise KeyError(position)
        grid_x, grid_y = alg2grid(position) # pylint: disable=unbalanced-tuple-unpacking
        self.squares[grid_y][grid_x] = item
