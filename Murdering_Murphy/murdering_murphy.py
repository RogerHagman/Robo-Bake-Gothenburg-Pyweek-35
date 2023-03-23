"""Murdering Murphy"""
VERSION = '0.31 ALPHA'

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
GRID_WIDTH = GRID_HEIGHT = random.randint(2,10)
GRID_MARGIN = 0
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
        pygame.draw.rect(screen, (WHITE), [GRID_MARGIN + col * CELL_SIZE, GRID_MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE], 1)

class GameMap():
    """"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for y in range(height)] for x in range(width)]
    def set_cell(self, x, y, value):
        self.grid[y][x] = value

    def get_cell(self, x, y):
        """returns the state of a given cell"""
        return self.grid[y][x]

    def is_cell_empty(self, x, y):
        """Checks to see if a grid element is empty / has value = 0"""
        return self.grid[y][x] == 0
    def display_map(self):
        """Prints out the current positions"""
        [print(' '.join(str(gamemap.get_cell(j, i)) for j in range(GRID_WIDTH))) for i in range(GRID_HEIGHT)]

class GameObject(pygame.sprite.Sprite):
    """A Superclass for all game objects extends pygame.sprite.Sprite"""
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
    """Holds information about player objects. Player has x,y positions and a marker/color"""
    def __init__(self,x,y):
        super(Player, self).__init__(x,y, GREEN)

    # Move the sprite based on keypresses
    def update(self, pressed_keys, gamemap):
        """Listens for keypresses and updates accordingly with Delta (X,Y) values """
        delta_x, delta_y = 0, 0

        if pressed_keys[pygame.K_UP] and self.y > 0:
            delta_y = -1

        elif pressed_keys[pygame.K_DOWN] and self.y < GRID_HEIGHT - 1:
            delta_y = 1

        elif pressed_keys[pygame.K_LEFT] and self.x > 0:
            delta_x = -1

        elif pressed_keys[pygame.K_RIGHT] and self.x < GRID_WIDTH - 1:
            delta_x = 1
        
        # Old map position emtied
        gamemap.set_cell(self.x, self.y, 0)
        # Moves the player in the desired direction by adding delta to the absolute position
        self.x += delta_x
        self.y += delta_y
        # Populates the players new position on the map
        gamemap.set_cell(self.x, self.y, 1)
        # The object marker is moved on the game screen
        self.rect.move_ip(delta_x * CELL_SIZE, delta_y * CELL_SIZE)
        print(f"player is in: {self.x},{self.y}")
        # Displays the updated state of the map
        gamemap.display_map()

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.direction = (0, 0)
    def update(self, gamemap):
        # generate a random direction, with extra copies of the current direction
        directions = [self.direction] * 10 + [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = random.choice(directions)
        
        # update the current direction
        self.direction = (dx, dy)

        new_x, new_y = self.x + dx, self.y + dy

        # check if the new position is valid
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            # update the position of the enemy
            gamemap.set_cell(self.x, self.y, 0)
            self.x, self.y = new_x, new_y
            gamemap.set_cell(self.x, self.y, 8)
            self.rect.move_ip(dx * CELL_SIZE, dy * CELL_SIZE)
            cloaked = random.randint(1,1) 
            if cloaked > 1:
                self.surf.fill(BLACK)
            else:
                self.surf.fill(RED)
class Escape(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        x = self.x
        y = self.y
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
enemy_x, enemy_y = 0, 0
escape_x, escape_y = 0, 0
gamemap.set_cell(player_x, player_y, 1)

# Create our 'player'
player = Player(0,0)

print(f"player is in: {player_x},{player_y}")
gamemap.display_map()

event_test = Game_Events()

# Variable to keep our main loop running
running = True
pygame.image.save(screen,"gamemap.jpg")

bg_img = pygame.image.load("gamemap.jpg")
bg_img = pygame.transform.scale(bg_img,(WINDOW_HEIGHT,WINDOW_WIDTH))
door = pygame.image.load("gamemap.jpg")
door = pygame.transform.scale(door,((WINDOW_HEIGHT,WINDOW_WIDTH)))
knife = pygame.image.load("nurz.gif")
knife = pygame.transform.scale(knife,((CELL_SIZE,CELL_SIZE)))
# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

# A custom event to spawn the escape room on the map
EscapeROOM = pygame.USEREVENT + 2
pygame.time.set_timer(EscapeROOM, 1000)

MOVE_ENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(MOVE_ENEMY, 500)
# Groups for rendering the screen
enemies = pygame.sprite.Group()
escapes = pygame.sprite.Group()
doors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Variable to keep track of whether the enemy has spawned or not
escape_spawned = False
murphy_spawned = False
# The Main game loop
while running:
    screen.blit(bg_img,(0,0))
    # Set the timer for the MOVE_ENEMY event

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
        elif event.type == MOVE_ENEMY:
            # Update the position of enemies
            [enemy.update(gamemap) for enemy in enemies]

        # Has the EscapeROOM event been triggered?
        elif event.type == EscapeROOM:
            # Escape door
            door = pygame.image.load("double_door.png")
            door = pygame.transform.scale(door,(CELL_SIZE,CELL_SIZE))

            # If the escape room hasn't spawned yet
            if not escape_spawned:
                # Set the spawned flag to True
                escape_spawned = True
                # Spawn after x seconds
                time.sleep(1)
                # Generate random x and y coordinates within the game grid
                
                escape_x, escape_y = event_test.generate_valid_position(gamemap)
                # Escape object gets added to the game grid with the marker 4
                gamemap.set_cell(escape_x, escape_y, 4)
                
                # Create an Escape object and set its position to the random x and y coordinates
                escape = Escape(escape_x, escape_y)
                escape.rect.x = escape_x * CELL_SIZE
                escape.rect.y = escape_y * CELL_SIZE

                # door_sprite.rect = door_rect
                print(f"The Door is in: {escape_x},{escape_y}")
                # Add the escape object to the escapes and all_sprites groups
                escapes.add(escape)
                all_sprites.add(escape)
                
 
    # Update the position of Escapes
    [escape.update() for escape in escapes]
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    door_rect = pygame.Rect(escape_x * CELL_SIZE, escape_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(door, door_rect)
    murph_rect = pygame.Rect(enemy_x * CELL_SIZE, enemy_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(knife, murph_rect)
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

    # Checks to if the player has found the escape
    elif pygame.sprite.spritecollideany(player, escapes):
        print("You escaped Murdering Murpy congratulations!\n\nYOU WIN!")
        time.sleep(3)
        # If so, stop the loop
        running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()