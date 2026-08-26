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

def test_move_forward():
    game = _get_game(['a2a4', 'a7a5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a1a3'))
    assert game.board['a3'].piece is not None

def test_move_diagonally():
    game = _get_game(['a2a4', 'a7a5', 'a1a3', 'b7b5'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('a3b4'))

def test_capture():
    game = _get_game(['a2a4', 'a7a5', 'a1a3', 'b7b5', 'a3b3', 'b5b4'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('b3b4'))
