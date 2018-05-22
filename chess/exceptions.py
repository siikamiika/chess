"""Game exceptions"""

class IllegalMove(Exception):
    """An illegal piece move was attempted"""

class PlayerExists(Exception):
    """A player tried to choose a color that was already chosen"""
