import pytest

from chess.game import Chess, GameOver
from chess.colors import COLOR

def test_stalemate():
    game = Chess.from_file('test/stalemate.txt')
    black = game.players[COLOR.black]
    with pytest.raises(GameOver) as excinfo:
        black.move('b3', 'c2')
    assert str(excinfo.value) == 'Game over. Stalemate'
