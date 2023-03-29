import os
import sys

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PRINTER_COLOR = LIGHTGREY
DIALOGUE_CHOICE = BLUE

# Settings / Global variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
TITLE = 'Robo Bake Gothenburg'
ASSETS_PATH = os.path.join(sys.path[0], 'Assets')

SCENE_FONT = os.path.join(ASSETS_PATH, 'Roboto-Light.tff')

SCENE_FONT_SMALL = 20
SCENE_FONT_LARGE = 40

BGCOLOR = BLACK
FPS = 60

# Grids and Tiles
TILESIZE = 40
GRIDWIDTH = SCREEN_WIDTH / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 4

# Enemy settings
ENEMY_SPEED = 4

# Image paths
BG_IMG = os.path.join(ASSETS_PATH,"bg.png")
WALL_IMG = os.path.join(ASSETS_PATH,"wall.png")
PLAYER_IMG = os.path.join(ASSETS_PATH,"player.png")
DOOR_IMG = os.path.join(ASSETS_PATH,"door.png")
ENEMY1_IMG = os.path.join(ASSETS_PATH,"enemy1.png")
ENEMY2_IMG = os.path.join(ASSETS_PATH,"enemy2.png")
PIE_IMG = os.path.join(ASSETS_PATH,"pie.png")
PLANT_IMG = os.path.join(ASSETS_PATH,"plant.png")
PHONE_IMG = os.path.join(ASSETS_PATH,"phone.png")