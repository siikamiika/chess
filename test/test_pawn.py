import pytest

from chess import Chess, Player
from chess.colors import COLOR
from chess.exceptions import IllegalMove
from chess.piece.queen import Queen

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

def test_move_2_forward():
    game = _get_game()
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a2a4'))

def test_move_again():
    game = _get_game(['a2a4', 'h7h5'])
    with pytest.raises(IllegalMove):
        player = game.players[game.turn]
        player.move(*Chess.parse_move('a2a4'))

def test_move_1_forward_after_2_forward():
    game = _get_game(['a2a4', 'h7h5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a4a5'))

def test_move_backwards():
    game = _get_game(['a2a4', 'h7h5', 'a4a5', 'h5h4'])
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('a5a4'))

def test_move_capture_nothing():
    game = _get_game(['a2a4', 'h7h5'])
    with pytest.raises(IllegalMove):
        player = game.players[game.turn]
        player.move(*Chess.parse_move('a4b5'))

def test_move_along_rank():
    game = _get_game(['a2a4', 'h7h5', 'a4a5', 'h5h4'])
    with pytest.raises(IllegalMove):
        player = game.players[game.turn]
        player.move(*Chess.parse_move('a5b5'))

def test_move_out_of_bounds():
    game = _get_game()
    player = game.players[game.turn]
    with pytest.raises(IllegalMove):
        player.move(*Chess.parse_move('a2`2'))

def test_en_passant():
    game = _get_game(['a2a4', 'h7h5', 'a4a5', 'b7b5'])
    player = game.players[game.turn]
    player.move(*Chess.parse_move('a5b6'))
    assert game.board['b5'].piece is None
    assert game.board['b6'].piece is not None
    assert game.board['b6'].piece.color == COLOR.white

def test_promotion():
    game = _get_game(['a2a4', 'h7h5', 'a4a5', 'b7b5', 'a5b6', 'c7c5', 'b6b7', 'b8c6'])
    game.players[game.turn].move(*Chess.parse_move('b7b8q'))
    game.players[game.turn].move(*Chess.parse_move('a7a6'))
    game.players[game.turn].move(*Chess.parse_move('b8c8'))
    assert game.board['c8'].piece is not None
    assert game.board['c8'].piece.color == COLOR.white
    assert isinstance(game.board['c8'].piece, Queen)
