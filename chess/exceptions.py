"""Game exceptions"""

class IllegalMove(Exception):
    """An illegal piece move was attempted"""

class PlayerExists(Exception):
    """A player tried to choose a color that was already chosen"""

class NotYourTurn(Exception):
    """Wait for your turn"""

class NotYourPiece(Exception):
    """You can only move pieces of your color"""

class GameNotStarted(Exception):
    """Start the game first"""

class GameOver(Exception):
    """The game is over"""

class GameAlreadyStarted(Exception):
    """An action requiring the game to be waiting was attempted after starting it"""
