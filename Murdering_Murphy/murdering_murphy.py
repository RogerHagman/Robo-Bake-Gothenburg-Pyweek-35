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
grid_width = grid_height = 4
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
        if pressed_keys[K_UP] and player_y > 0:
            time.sleep(0.25)
            self.rect.move_ip(0, -cell_size)
            gamemap[player_y][player_x] = 0
            player_y -= 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_DOWN] and player_y < grid_height - 1:
            time.sleep(0.25)
            self.rect.move_ip(0, cell_size)
            gamemap[player_y][player_x] = 0
            player_y += 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_LEFT] and player_x > 0:
            time.sleep(0.25)
            self.rect.move_ip(-cell_size, 0)
            gamemap[player_y][player_x] = 0
            player_x -= 1
            gamemap[player_y][player_x] = 1
            print(f"player is in: {player_x},{player_y}")
            [print(f"{gamemap[i]}\n") for i in range(grid_height)]
        if pressed_keys[K_RIGHT] and player_x < grid_width - 1:
            time.sleep(0.25)
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
        self.rect = self.surf.get_rect()
    def update(self):
        pass

class Exit(pygame.sprite.Sprite):
    def __init__(self):
        super(Exit, self).__init__()
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()
    def update(self):
        pass

# Variable to keep our main loop running
running = True
pygame.image.save(screen,"gamemap.jpg")

bg_img = pygame.image.load("gamemap.jpg")
bg_img = pygame.transform.scale(bg_img,(window_size))

# Initialize Pygame
pygame.init()

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

# A custom event to spawn the exit room on the map
EXITROOM = pygame.USEREVENT + 2
pygame.time.set_timer(EXITROOM, 1000)

# Create our 'player'
player = Player()

# Groups for rendering the screen
enemies = pygame.sprite.Group()
exits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
                # Get the set of keys pressed and check for user input
                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys)

        # Has the ADDENEMY event been triggered?
        elif event.type == ADDENEMY:
            # If the enemy hasn't spawned yet
            if not murphy_spawned:
                # Set the spawned flag to True
                murphy_spawned = True
                # Spawn after x seconds
                time.sleep(1)
                # Generate random x and y coordinates within the game grid
                enemy_x = random.randint(0, grid_width - 1)
                enemy_y = random.randint(0, grid_height - 1)

                # Enemy object gets added to the game grid with the marker 8
                gamemap[enemy_y][enemy_x] = 8
                
                # Create an Enemy object and set its position to the random x and y coordinates
                enemy = Enemy()
                enemy.rect.x = enemy_x * cell_size
                enemy.rect.y = enemy_y * cell_size
                print(f"Murphy has spawned in: {enemy_x},{enemy_y}")
                
                # Add the Enemy object to the enemies and all_sprites groups
                enemies.add(enemy)
                all_sprites.add(enemy)

        # Has the EXITROOM event been triggered?
        elif event.type == EXITROOM:
            # If the exit room hasn't spawned yet
            if not exit_spawned:
                # Set the spawned flag to True
                exit_spawned = True
                # Spawn after x seconds
                time.sleep(1)
                # Generate random x and y coordinates within the game grid
                exit_x = random.randint(0, grid_width - 1)
                exit_y = random.randint(0, grid_height - 1)

                # Enemy object gets added to the game grid with the marker 8
                gamemap[exit_y][exit_x] = 4
                
                # Create an Enemy object and set its position to the random x and y coordinates
                exit = Exit()
                exit.rect.x = exit_x * cell_size
                exit.rect.y = exit_y * cell_size
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
    if pygame.sprite.spritecollideany(player, exits):
        print("You escaped Murpy congratulations!\n\nYOU WIN!")
        time.sleep(3)
        # If so, stop the loop
        running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
