import pygame
from os import path
from settings import *
import random
pygame.mixer.init()
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
        self.radius = TILESIZE

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
        
        self.pies = 0
        self.total_pies = 0
        self.love = 0
        self.sound = pygame.mixer.Sound(PLAYER_SOUND)
    def update(self, screen_dimensions, walls, doors, enemies):
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

        # check if player has picked up a pie and increase their speed
        if self.pies == 0:
            self.speed = 1
        elif self.pies == 1:
            self.speed = 2
        elif self.pies == 5:
            self.speed = 3
        elif self.pies == 10:
            self.speed = 4
        elif self.pies == 15:
            self.speed = 5
        elif self.pies == 26:
            self.love = 12
            print("BAKERS DOZEN: ACHIEVEMENT UNLOCKED!")
        # Update the player's position based on the delta values and speed.
        old_x, old_y = self.get_position()
        future_x, future_y = (old_x + delta_x * self.speed, old_y + delta_y * self.speed)
        future_rect = self.rect.move(delta_x * self.speed, delta_y * self.speed)

        # Check if the player has moved and play the sound if they have.
        # if (future_x, future_y) != (old_x, old_y):
        #     self.sound.play()

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
         # Check for collisions with enemy objects
        for enemy in enemies:
            if future_rect.colliderect(enemy.rect):
                #If collision with an enemy occurs the printer gets captured and the game should end.
                self.is_alive = False
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
        pass

    def get_pie_love(self):
        return self.pies, self.total_pies, self.love
    def eat_pie(self):
        self.pies += 1
        self.total_pies +=1
    def purge_pies(self):
        self.pies = 0
    def set_love(self, love):
        self.love += love
        
class Enemy(GameObject):
    """A class for Moving Enemy Characters"""
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.direction = (0, 0)
        self.speed = ENEMY_SPEED
        self.freeze_time = 0
        self.sound = pygame.mixer.Sound(ENEMY_TALK)
        self.sound_playing = False
        self.sound_channel = pygame.mixer.Channel(0)

    def update(self, screen_dimensions, walls, distractions):
        if self.freeze_time > 0:
            self.freeze_time -= 1
            return self.freeze_time // FPS  # Enemy should not move while it's frozen
        else:
            # Generates a random direction, with extra copies of the current direction
            directions = [self.direction] * 100 + [(1, 0), (-1, 0), (0, 1), (0, -1)]
            delta_x, delta_y = random.choice(directions)

            # Updates the current direction
            self.direction = (delta_x, delta_y)

            # Calculates the new position of the enemy
            new_x, new_y = self.x + delta_x, self.y + delta_y

            # Checks if the new position is a valid one
            if 0 <= new_x < screen_dimensions[0] and 0 <= new_y < screen_dimensions[1]:
                # Check for collisions with wall objects
                for wall in walls:
                    if pygame.Rect(new_x, new_y, self.rect.width, self.rect.height).colliderect(wall.rect):
                        # The enemy collided with a wall, so it should not move.
                        break
                else:
                    # The enemy did not collide with any walls, so it can move to the new position.
                    self.set_position(new_x, new_y)
                # Check for collisions with distraction objects
                for distraction in distractions:
                    if pygame.Rect(new_x, new_y, self.rect.width, self.rect.height).colliderect(distraction.rect):
                        # The enemy collided with a distraction causing it to freeze for ENEMY_DISTRACT_TIME seconds
                        distraction.phone_ring()
                        self.sound_playing = True
                        self.sound_channel.play(self.sound)
                        self.freeze_time = (random.randint(0,10) + ENEMY_DISTRACT_TIME) * FPS
                        self.direction = (-self.direction[0], -self.direction[1])  # Reverse direction
                        break

            # Check if the sound has stopped playing and update self.sound_playing accordingly
            if self.sound_playing and self.freeze_time <= (1 * FPS) and not self.sound_channel.get_busy():
                self.sound_playing = False

            return self.freeze_time // FPS
class Wall(GameObject):
    """A class for wall objects."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        #x = self.x                     NB
        #y = self.y
        self.is_windowed = False
    def update(self, x,y):
        pass

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


class Pie(GameObject):
    """
    A table with a pie, until eaten, then it's just a table.
    """
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.eaten = False
    
    def eat(self):
        self.eaten = True
        self.figure = pygame.transform.scale(pygame.image.load(TABLE_IMG),(TILESIZE*0.8,TILESIZE*0.8))
    
    def is_eaten(self):
        return self.eaten
    
class Distraction(GameObject):
    """
    The phone rings. Brr. Brr.
    Unclear if this needs methods, perhaps simply a
    separate group of Clutter objects would work just as well.
    But just in case we discover it needs a method...
    """
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.sound = pygame.mixer.Sound(PHONE_SOUND)
        self.sound_channel = pygame.mixer.Channel(1)
        self.last_ringing_time = 0
    def phone_ring(self):
        sound_channel = pygame.mixer.Channel(1)  # Find an available sound channel
        sound_channel.set_volume(0.15)  # Set the volume of the sound channel
        sound_channel.play(self.sound)  # Play the ring sound on the channel
class Clutter(GameObject):
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)