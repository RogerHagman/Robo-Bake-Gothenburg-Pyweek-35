import pygame
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """ """
    pass
class Level():
    """ """
    pass
class Menu():
    """ """
    pass
class GameObject(pygame.sprite.Sprite):
    """ A superclass for all game objects, extends pygame.sprite.Sprite. """
    def __init__(self, x, y, figure):
        """

        @params: 
        x - horizontal position
        y - vertical position
        figure - figure object (like image or shape)

        """
        super().__init__()
        self.figure = figure
        # I think this should with something like tile_size
        self.surf = pygame.Surface((figure.get_width(), figure.get_height()))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.x, self.y = x, y

    def update(self):
        """Update the object's state each frame."""
        pass
    
    def draw(self, screen):
        """Draw an object on the screen."""
        screen.blit(self.figure, (self.x, self.y))

    def get_position(self):
        """Get the object's position as a tuple of (x, y) screen coordinates."""
        return self.x, self.y

    def get_figure_shape(self):
        """Get the object's figure object."""
        return self.figure

class Player(GameObject):
    """A class for the main character."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.speed = 5

    def update(self, pressed_keys, screen_dimensions):
        """Update the player's position based on key presses and the game's state."""
        delta_x, delta_y = 0, 0

        if pressed_keys[pygame.K_UP] and self.y > 0:
            delta_y = -1

        elif pressed_keys[pygame.K_DOWN] and self.y < screen_dimensions[1] - 1:
            delta_y = 1

        elif pressed_keys[pygame.K_LEFT] and self.x > 0:
            delta_x = -1

        elif pressed_keys[pygame.K_RIGHT] and self.x < screen_dimensions[0] - 1:
            delta_x = 1

        # Update the player's position based on the delta values and speed.
        self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)

    def collision(self, other):
        if isinstance(other, Wall):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            self.rect.topleft = pos_before_col
            # Set the player's speed to 0
            self.speed = 0

class Wall(GameObject):
    """A class for wall objects."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        x = self.x
        y = self.y

    def update(self, x,y):
        self.x = x
        self.y = y

    def get_position(self):
        """returns the walls position as (x, y) screen coordinates."""
        return self.x, self.y

class Hud(GameObject):
    """ """
    pass
class Map():
    """ """
    pass

class Dialogues():
    """ """
    pass