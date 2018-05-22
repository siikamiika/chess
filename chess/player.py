"""A chess player"""

class Player(object):
    """The player"""
    def __init__(self, color):
        self.color = color
        self.game = None
