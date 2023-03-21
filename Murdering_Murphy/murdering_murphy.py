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
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Gridmap parameters
grid_width = grid_height = 5
grid_margin = 0
cell_size = int(WINDOW_HEIGHT / grid_height) if WINDOW_WIDTH > WINDOW_HEIGHT else int(WINDOW_WIDTH / grid_width)

# Setup game window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Murdering Murphy")

# Nested forloop to draw the grid
for row in range(grid_height):
    for col in range(grid_width):
        pygame.draw.rect(screen, (255, 255, 255), [grid_margin + col * cell_size, grid_margin + row * cell_size, cell_size, cell_size], 1)

# The game map coordinates initialized
gamemap = []

for x in range(grid_width):
    gamemap.append([])
    for y in range(grid_height):
        gamemap[-1].append(0)

# Giving the player x and y coordinates and positioning them on the map
player_x, player_y = (0,0)
gamemap[player_y][player_x] = 1

print(f"player is in: {player_x},{player_y}")
[print(f"{gamemap[i]}\n") for i in range(grid_height)]

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        global player_x, player_y
        global gamemap
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -cell_size)
            gamemap[player_y][player_x] = 0
            player_y -= 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, cell_size)
            gamemap[player_y][player_x] = 0
            player_y += 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-cell_size, 0)
            gamemap[player_y][player_x] = 0
            player_x -= 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(cell_size, 0)
            gamemap[player_y][player_x] = 0
            player_x += 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
        )
        
# Variable to keep our main loop running
running = True
pygame.image.save(screen,"gamemap.jpg")

bg_img = pygame.image.load("gamemap.jpg")
bg_img = pygame.transform.scale(bg_img,(window_size))

# Initialize Pygame
pygame.init()

# Create our 'player'
player = Player()

# Creates Murphy
murphy = Enemy()

# Groups for rendering the screen
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(murphy)
# The Main game loop
while running:
    screen.blit(bg_img,(0,0))
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            time.sleep(0.1)
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

    # If the user clicks the close window button the game is exited.
        elif event.type == QUIT:
            running = False
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the screen
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()