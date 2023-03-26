import pygame

"""
Example of OOP structure
"""

class Game():
    def __init__(self) -> None:
        """
        Initialize display, game objects and states
        """
        pass

    def render(self):
        """
        Blit game objects onto display
        """
        pass

    def run(self):
        """
        While loop that handles events and calls render(self)
        """
        pass

class GameObject(pygame.sprite.Sprite):
    """
    Has a surface, rect, and position we can access to render object
    """


class Walker(GameObject):
    """
    GameObject class with animation logic
    """
    
class Player(Walker):
    """
    Animated game object representing player
    Unique attributes for eg health, inventory etc
    """

class Map():
    """
    For generating a game map
    """

class Hud():
    """
    Area outside of map for eg health bars and game information
    """