"""Piece and terminal colors"""
from enum import Enum
import colorama

COLOR = Enum('COLOR', ('white', 'black'))

BG1 = colorama.Back.WHITE
BG2 = colorama.Back.LIGHTBLACK_EX
FG_WHITE = colorama.Fore.LIGHTWHITE_EX
FG_BLACK = colorama.Fore.BLACK
RESET_STYLE = colorama.Style.RESET_ALL
