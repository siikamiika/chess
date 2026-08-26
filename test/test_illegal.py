import pytest

from chess.exceptions import IllegalMove
from chess.game import Chess
from chess.colors import COLOR

def test_checkmate():
    with pytest.raises(IllegalMove) as excinfo:
        Chess.from_file('test/illegal.txt')
    assert str(excinfo.value) == "('e2', 'e5')"
