import pygame
from os import path
from settings import *
import random

class GameObject(pygame.sprite.Sprite):
    """ A superclass for all game objects, extends pygame.sprite.Sprite. """
    def __init__(self, x, y, figure):
        """
        params: 
        @x - horizontal position
        @y - vertical position
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
    
    def set_position(self, x, y):
        self.x, self.y = x, y
        self.rect.update((x,y),(self.rect.size))        #NB, kim har pillat

    def get_figure_shape(self):
        """Get the object's figure object."""
        return self.figure

class Player(GameObject):
    """A class for the main character."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.speed = PLAYER_SPEED
        # This flips to False if player exits a level/finishes the game or gets hit by an enemy.
        self.is_alive = True
        self.is_exited = False
        self.is_win = False
    
    def update(self, screen_dimensions, walls, doors):
        """Update the player's position based on key presses and the game's state."""
        delta_x, delta_y = 0, 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.y > 0:
            delta_y = -PLAYER_SPEED

        if pressed_keys[pygame.K_DOWN] and self.y < screen_dimensions[1] - 1:
            delta_y = PLAYER_SPEED

        if pressed_keys[pygame.K_LEFT] and self.x > 0:
            delta_x = -PLAYER_SPEED

        if pressed_keys[pygame.K_RIGHT] and self.x < screen_dimensions[0] - 1:
            delta_x = PLAYER_SPEED

        # if delta_x != 0 and delta_y != 0:
        #     delta_x *= 0.7071
        #     delta_y *= 0.7071
        
        # Update the player's position based on the delta values and speed.
        old_x, old_y = self.get_position()
        future_x, future_y = (old_x + delta_x * self.speed, old_y + delta_y * self.speed)
        future_rect = self.rect.move(delta_x * self.speed, delta_y * self.speed)

        # Check for collisions with wall objects
        for wall in walls:
            if future_rect.colliderect(wall.rect):
                # Set the player's position to the old position to prevent collision with the wall
                future_x, future_y = old_x, old_y
                future_rect = self.rect.move(0, 0)
                break
        # Check for collisions with door objects
        for door in doors:
            if future_rect.colliderect(door.rect):
                future_x, future_y = old_x, old_y
                future_rect = self.rect.move(0, 0)
                self.is_exited = True
                break
        self.set_position(future_x, future_y)
        self.rect = future_rect

    def get_player_state(self):
        """
        Returns a tuple of player states
        params:     @is_alive: bool, 
                    @is_exited: bool,
                    @is_win: bool
        """
        return self.is_alive, self.is_exited, self.is_win

    def set_player_state(self, is_alive, is_exited, is_win):
        """Accepts a tuple of player states"""
        self.is_alive = is_alive
        self.is_exited = is_exited
        self.is_win = is_win
    
    def player_is_win(self):
        self.is_alive, self.is_exited, self.is_win = self.set_player_state(True,True, True)
        return "You win the game"
    def collision(self, other):
        if isinstance(other, Wall):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            self.rect.topleft = pos_before_col
            # Set the player's speed to 0
            #self.speed = 0
            print(f"Wall x:{other.rect.x}, Wall y:{other.rect.y}")

        elif isinstance(other, Door):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            # Player Exits the current Map if it is the last door, the player wins. 
            # If it is not game continues on next level
            if Door.get_last_door():
                self.set_player_state = (True, True, True)
            else:
                self.set_player_state = (True, True, False)
        elif isinstance(other, Enemy):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            # Player dies and looses the game
            self.set_player_state = (False, True, False)

class Enemy(GameObject):
    """A class for Moving Enemy Characters"""
    def __init__(self, x, y,figure):
        super().__init__(x, y, figure)
        self.direction = (0, 0)
        self.speed = ENEMY_SPEED

    def update(self, screen_dimensions):
        # Generates a random direction, with extra copies of the current direction
        directions = [self.direction] * 100 + [(1, 0), (-1, 0), (0, 1), (0, -1)]
        delta_x, delta_y = random.choice(directions)
        
        # Updates the current direction
        self.direction = (delta_x, delta_y)

        new_x, new_y = self.x + delta_x, self.y + delta_y

        # Checks if the new position is a valid one
        if 0 <= new_x < screen_dimensions[0]and 0 <= new_y < screen_dimensions[1]:
            # Update the position of the enemy

            self.x, self.y = new_x, new_y

            self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)
 
class Wall(GameObject):
    """A class for wall objects."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        #x = self.x                     NB
        #y = self.y
        self.is_windowed = False
    def update(self, x,y):
        self.x = x
        self.y = y

    def set_windowed(self, window):
        self.is_windowed = window

    def get_windowed(self):
        return self.is_windowed

class Door(GameObject):
    """Class for defining exit points on the Map."""
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        # x = self.x
        # y = self.y
        
    def set_last_door(self, last_door):
        self.is_last_door = last_door

    def get_last_door(self):
        return self.get_last_door
    
    def update(self):
        pass
