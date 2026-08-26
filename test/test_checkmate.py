import pytest

from chess.game import Chess, GameOver
from chess.colors import COLOR

def test_checkmate():
    game = Chess.from_file('test/checkmate.txt')
    black = game.players[COLOR.black]
    with pytest.raises(GameOver) as excinfo:
        black.move('f2', 'h2')
    assert str(excinfo.value) == 'Game over. Black wins'
