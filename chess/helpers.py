"""Often needed functions"""
import re

def alg2grid(alg):
    """Convert algebraic notation to grid indices"""
    out = []
    for char in alg:
        if 'a' <= char <= 'h':
            out.append(ord(char) - 0x61)
        elif '1' <= char <= '8':
            out.append((7 - ord(char)) + 0x31)
        else:
            raise ValueError

    return out

def grid2alg(grid_x=None, grid_y=None):
    """Convert grid indices to algebraic notation"""
    return (
        chr(0x61 + grid_x) if grid_x is not None else '',
        chr(7 - grid_y + 0x31) if grid_y is not None else '',
    )

def algdelta(alg1, alg2, *args):
    """Rank and file difference between two moves in algebraic notation"""
    file_delta = ord(alg2[0]) - ord(alg1[0])
    rank_delta = ord(alg2[1]) - ord(alg1[1])
    return file_delta, rank_delta

POS_PATTERN = re.compile(r'^[a-h][1-8]$')
def is_position(position):
    """Check if position is a valid position on the chessboard"""
    return isinstance(position, str) and len(position) == 2 and POS_PATTERN.match(position)

def char_range(c1, c2):
    """Generates the characters between c1 and c2, inclusive.
    Autodetects reversed range."""
    step = 1
    start, end = ord(c1), ord(c2)
    if start > end:
        step = -1
    for charcode in range(start, end + step, step):
        yield chr(charcode)
