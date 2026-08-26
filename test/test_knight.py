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

def test_knight_move():
    game = _get_game()
    player = game.players[game.turn]
    player.move(*Chess.parse_move('b1c3'))

def test_knight_2_forward():
    game = _get_game()
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('b1b3'))

def test_knight_capture():
    game = _get_game(['b1c3', 'g8f6', 'c3b5', 'h7h5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('b5c7'))

def test_knight_out_of_bounds():
    game = _get_game(['b1c3', 'g8f6', 'c3b5', 'e7e5', 'b5c7', 'e8e7'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('c7b9'))
