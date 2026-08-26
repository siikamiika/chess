import pytest

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import IllegalMove

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

def test_move_through_own_piece():
    game = _get_game(['c2c3', 'd7d6'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('c1a3'))

def test_move_diagonally():
    game = _get_game(['c2c3', 'd7d6', 'b2b3', 'h7h5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('c1a3'))
    assert game.board['a3'].piece is not None

def test_move_forward():
    game = _get_game(['c2c3', 'd7d6', 'b2b3', 'h7h5'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('c1c2'))

def test_capture():
    game = _get_game(['c2c3', 'd7d6', 'b2b3', 'h7h5', 'c1a3', 'h5h4'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a3d6'))
    assert game.board['d6'].piece is not None
