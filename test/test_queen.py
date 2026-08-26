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

def test_queen_move_through_own_piece():
    game = _get_game(['d2d3', 'd7d6'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('d1d4'))

def test_queen_move_like_a_knight():
    game = _get_game(['d2d3', 'd7d6'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('d1e3'))

def test_queen_capture_behind_piece():
    game = _get_game(['d2d3', 'd7d6'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('d1d6'))

def test_queen_valid_capture():
    game = _get_game(['d2d3', 'd7d6', 'c2c3', 'c7c6', 'd1a4', 'd6d5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a4c6'))
    assert game.board['c6'].piece is not None
