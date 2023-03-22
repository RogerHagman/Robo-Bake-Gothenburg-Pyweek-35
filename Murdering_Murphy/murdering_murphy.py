"""Murdering Murphy"""
VERSION = '0.2 ALPHA'

# Imports
import pygame
import random
import time

# Keyboard commands
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Display Constancts
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Gridmap parameters
GRID_WIDTH = GRID_HEIGHT = 5
grid_margin = 0
CELL_SIZE = int(WINDOW_HEIGHT / GRID_HEIGHT) if WINDOW_WIDTH > WINDOW_HEIGHT else int(WINDOW_WIDTH / GRID_WIDTH)

# Colors
WHITE   =    (255, 255, 255)
BLACK   =    (0, 0, 0)
RED     =    (255, 0, 0)
GREEN   =    (0, 255, 0)
YELLOW  =    (255, 255, 0)

# Initialize Pygame
pygame.init()

# Setup game window
screen = pygame.display.set_mode((WINDOW_HEIGHT,WINDOW_WIDTH))
pygame.display.set_caption("Murdering Murphy")

# Nested forloop to draw the grid
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        pygame.draw.rect(screen, (WHITE), [grid_margin + col * CELL_SIZE, grid_margin + row * CELL_SIZE, CELL_SIZE, CELL_SIZE], 1)

class GameMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for y in range(height)] for x in range(width)]
        print(self.grid)
    def set_cell(self, x, y, value):
        self.grid[y][x] = value

    def get_cell(self, x, y):
        return self.grid[y][x]

    def is_cell_empty(self, x, y):
        return self.grid[y][x] == 0

class GameObject(pygame.sprite.Sprite):
    """A Superclass for all game objects"""
    def __init__(self, x, y, color):
        super().__init__()
        self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft=(x * CELL_SIZE, y * CELL_SIZE))
        self.x, self.y = x, y

    def update(self):
        pass

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(GameObject):
    def __init__(self,x,y):
        super(Player, self).__init__(x,y, GREEN)

    # Move the sprite based on keypresses
    def update(self, pressed_keys, gamemap):
        """Listens for keypresses and updates accordingly with Delta (X,Y) values """
        delta_x, delta_y = 0, 0

        if pressed_keys[pygame.K_UP] and self.y > 0:
            delta_y = -1

            # MAP MOVEMENT
            gamemap.set_cell(self.x, self.y, 0)
            print(f"player is in: {self.x},{self.y}")

        elif pressed_keys[pygame.K_DOWN] and self.y < GRID_HEIGHT - 1:
            delta_y = 1

            # MAP MOVEMENT
            gamemap.set_cell(self.x, self.y, 0)
            print(f"player is in: {self.x},{self.y}")

        elif pressed_keys[pygame.K_LEFT] and self.x > 0:
            delta_x = -1

            # MAP MOVEMENT
            gamemap.set_cell(self.x, self.y, 0)
            print(f"player is in: {self.x},{self.y}")

        elif pressed_keys[pygame.K_RIGHT] and self.x < GRID_WIDTH - 1:
            delta_x = 1

            # MAP MOVEMENT
            gamemap.set_cell(self.x, self.y, 0)
            print(f"player is in: {self.x},{self.y}")
        
        # Moves the player in the desired direction by adding delta to the absolute position
        self.x += delta_x
        self.y += delta_y
        gamemap.set_cell(self.x, self.y, 1)
        self.rect.move_ip(delta_x * CELL_SIZE, delta_y * CELL_SIZE)
        # Print out the the updated positions
        [print(' '.join(str(gamemap.get_cell(j, i)) for j in range(GRID_WIDTH))) for i in range(GRID_HEIGHT)]

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, RED)

    def update(self):
        pass

class Exit(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)

    def update(self):
        pass

class Game_Events():
        
    def __init__(self):
        pass

    def generate_valid_position(self, gridmap):
        """Takes a gridmap as argument and randomely itterates the map until it finds a valid grid position (value == 0) """
        obj_x = random.randint(0, GRID_WIDTH - 1)
        obj_y = random.randint(0, GRID_HEIGHT - 1)
    
        while not gridmap.is_cell_empty(obj_x, obj_y):
            obj_x = random.randint(0, GRID_WIDTH - 1)
            obj_y = random.randint(0, GRID_HEIGHT - 1)

        return (obj_x, obj_y)

# Initialize the game map
gamemap = GameMap(GRID_WIDTH, GRID_HEIGHT)


# Giving the player x and y coordinates and positioning them on the map
player_x, player_y = (0, 0)
gamemap.set_cell(player_x, player_y, 1)

# Create our 'player'
player = Player(0,0)

print(f"player is in: {player_x},{player_y}")
# [print(f"{gamemap[i]}\n") for i in range(GRID_HEIGHT)]

event_test = Game_Events()

# Variable to keep our main loop running
running = True
pygame.image.save(screen,"gamemap.jpg")

bg_img = pygame.image.load("gamemap.jpg")
bg_img = pygame.transform.scale(bg_img,(WINDOW_HEIGHT,WINDOW_WIDTH))
door = pygame.image.load("gamemap.jpg")
door = pygame.transform.scale(door,((WINDOW_HEIGHT,WINDOW_WIDTH)))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

# A custom event to spawn the exit room on the map
EXITROOM = pygame.USEREVENT + 2
pygame.time.set_timer(EXITROOM, 1000)


# Groups for rendering the screen
enemies = pygame.sprite.Group()
exits = pygame.sprite.Group()
doors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

exit_x, exit_y = 0, 0

# Variable to keep track of whether the enemy has spawned or not
exit_spawned = False
murphy_spawned = False
# The Main game loop
while running:
    screen.blit(bg_img,(0,0))
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            else:
                # Check to se if a key has been pressed and if so execute that command
                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys, gamemap)

        # Has the ADDENEMY event been triggered?
        elif event.type == ADDENEMY:
            # If the enemy hasn't spawned yet
            if not murphy_spawned:
                # Set the spawned flag to True
                murphy_spawned = True
                # Spawn after x seconds
                time.sleep(1)
                # Generates random X,Y coordinates within the game grid that has not previously been filled with other objects
                enemy_x, enemy_y = event_test.generate_valid_position(gamemap)

                # Enemy object gets added to the game grid with the marker 8
                gamemap.set_cell(enemy_x, enemy_y, 8)
                
                # Create an Enemy object and set its position to the random x and y coordinates
                enemy = Enemy(enemy_x, enemy_y)
                enemy.rect.x = enemy_x * CELL_SIZE
                enemy.rect.y = enemy_y * CELL_SIZE
                print(f"Murphy has spawned in: {enemy_x},{enemy_y}")
                
                # Add the Enemy object to the enemies and all_sprites groups
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy.update()

        # Has the EXITROOM event been triggered?
        elif event.type == EXITROOM:
            # Exit door
            door = pygame.image.load("double_door.png")
            door = pygame.transform.scale(door,(CELL_SIZE,CELL_SIZE))

            # If the exit room hasn't spawned yet
            if not exit_spawned:
                # Set the spawned flag to True
                exit_spawned = True
                # Spawn after x seconds
                time.sleep(1)
                # Generate random x and y coordinates within the game grid
                exit_x, exit_y = event_test.generate_valid_position(gamemap)
                # Exit object gets added to the game grid with the marker 4
                gamemap.set_cell(exit_x, exit_y, 4)
                
                # Create an Exit object and set its position to the random x and y coordinates
                exit = Exit(exit_x, exit_y)
                exit.rect.x = exit_x * CELL_SIZE
                exit.rect.y = exit_y * CELL_SIZE

                # door_sprite.rect = door_rect
                print(f"The Door is in: {exit_x},{exit_y}")
                # Add the exit object to the exits and all_sprites groups
                exits.add(exit)
                all_sprites.add(exit)
                
    # Update the position of enemies
    [enemy.update() for enemy in enemies]
    # Update the position of Exits
    [exit.update() for exit in exits]
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    door_rect = pygame.Rect(exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(door, door_rect)
    # Create a rectangle to define the portion of the image to be drawn
    
    # Draw the door image onto the screen using the rectangle
    
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        print("Murphy has stabbed you in the eye with a butterknife, blood is pouring out of your eye socket, YOU REQUIRE IMEDIATE MEDICAL ASSISTANCE!")
        time.sleep(2.5)
        print("Bleeding...")
        time.sleep(2.5)
        print("Bleeding...")
        time.sleep(5)
        print("You have died from bleeding out\n\nGAME OVER")
        time.sleep(2)
        # If so, stop the loop
        running = False

    # Checks to if the player has found the exit
    elif pygame.sprite.spritecollideany(player, exits):
        print("You escaped Murdering Murpy congratulations!\n\nYOU WIN!")
        time.sleep(3)
        # If so, stop the loop
        running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()