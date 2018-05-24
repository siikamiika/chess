"""Implementation for pawn"""
from . import Piece, Queen
from ..colors import COLOR
from ..helpers import algdelta
from ..exceptions import IllegalMove

class Pawn(Piece):
    """A pawn of either color"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = {
            COLOR.white: '♙',
            COLOR.black: '♟',
        }[COLOR.black] # black as in fill entire symbol

    def can_capture(self, position):
        """Pawns can't capture everything they can move to, so this has to be overridden"""
        file_delta, rank_delta = algdelta(self.position, position)
        if abs(file_delta) == 1:
            if rank_delta == 1 if self.color == COLOR.white else rank_delta == -1:
                return True

    def move(self, position, commit=True):
        """Try to legally move the pawn to `position` and return the piece it captures,
        if captures"""
        captured = None
        file_delta, rank_delta = algdelta(self.position, position)
        # the pawn moves 1 to right or left, in an attempt to capture a piece...
        if abs(file_delta) == 1:
            # ...while moving 1 forward
            if rank_delta == 1 if self.color == COLOR.white else rank_delta == -1:
                for capture_func in self._check_en_passant, self._check_capture:
                    potential_capture = capture_func(position)
                    if potential_capture:
                        captured = potential_capture
                        break
                else:
                    raise IllegalMove(f'Nothing to capture at {position}')
            else:
                raise IllegalMove((self.position, position))
        # the pawn doesn't move to right or left...
        elif file_delta == 0:
            if (    # while moving 2 forward...
                    (not self.moves and # ...as its first move
                     (rank_delta == 2 if self.color == COLOR.white else rank_delta == -2)) or
                    # while moving 1 forward
                    (rank_delta == 1 if self.color == COLOR.white else rank_delta == -1)
                ):
                piece = self._move_parallel(position)
                if piece:
                    raise IllegalMove(f'There is a piece at {position}')
            else:
                raise IllegalMove((self.position, position))
        else:
            raise IllegalMove((self.position, position))

        super().move(position, commit=commit)
        if commit:
            self._check_promotion(position)

        return captured

    def _check_promotion(self, position):
        if position[1] == '8' if self.color == COLOR.white else position[1] == '1':
            # clone attributes
            piece = Queen(self.color) # TODO: underpromotion
            piece.game = self.game
            piece.position = self.position
            piece.moves = self.moves
            piece.piece_id = self.piece_id
            self.promoted_piece = piece

    def _check_capture(self, position):
        square = self.game.board[position]
        if square.piece and square.piece.color != self.color:
            return square.piece

    def _check_en_passant(self, position):
        other_position = position[0] + self.position[1]
        square = self.game.board[other_position]
        other_move = square.piece and square.piece.moves and square.piece.moves[0]

        if ( # pylint: disable=too-many-boolean-expressions
                other_move                                and # the piece in square has moved
                isinstance(square.piece, Pawn)            and # it is a pawn
                square.piece.color != self.color          and # it is the opponent
                len(square.piece.moves) == 1              and # it is its first move
                other_move[2] == len(self.game.moves) - 1 and # the move was the previous move
                abs(algdelta(*other_move)[1]) == 2            # the move was 2 forward
            ):
            return square.piece
