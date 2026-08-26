import pytest

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import IllegalMove
from chess.piece import King, Rook

def _get_game(moves=[]):
    game = Chess()
    player1 = Player(COLOR.white)
    player2 = Player(COLOR.black)
    game.add_player(player1)
    game.add_player(player2)
    game.start()
    for move in moves:
        player = game.players[game.turn]
        player.move(*Chess.parse_move(move))
    return game

def test_king_move_through_own_piece():
    game = _get_game()
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('e1e2'))

def test_king_move_out_of_bounds():
    game = _get_game()
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('e1e0'))

def test_king_move_2_squares():
    game = _get_game(['e2e4', 'e7e5'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('e1e3'))

def test_castle():
    game = _get_game(['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1d3', 'h7h5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('e1g1'))
    assert game.board['g1'].piece is not None
    assert game.board['f1'].piece is not None
    assert game.board['e1'].piece is None
    assert game.board['h1'].piece is None
    assert game.board['g1'].piece.color == COLOR.white
    assert game.board['f1'].piece.color == COLOR.white
    assert isinstance(game.board['g1'].piece, King)
    assert isinstance(game.board['f1'].piece, Rook)
    