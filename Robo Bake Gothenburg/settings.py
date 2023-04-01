import os
import sys

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (60, 60, 60)
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

# Grids and Tiles
TILESIZE = SCREEN_HEIGHT // 20
GRIDWIDTH = SCREEN_WIDTH / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE

# Fonts
SCENE_FONT = os.path.join(ASSETS_PATH, 'Roboto-Light.ttf')
SCENE_FONT_TINY = TILESIZE//4
SCENE_FONT_SMALL = TILESIZE//2
SCENE_FONT_MEDIUM = TILESIZE//2 + TILESIZE//4 + TILESIZE//8
SCENE_FONT_LARGE = TILESIZE

BGCOLOR = BLACK
FPS = 60

# Player settings
PLAYER_SPEED = 1

# Enemy settings
ENEMY_SPEED = 2
ENEMY_DISTRACT_TIME = 10

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
DESK_IMG = os.path.join(ASSETS_PATH,"desk1.png")
TABLE_IMG = os.path.join(ASSETS_PATH,"lonely_table.png")
LONE_PIE_IMG = os.path.join(ASSETS_PATH,"lonely_pie.png")
HEART_IMG = os.path.join(ASSETS_PATH,"heart.png")
FOG_IMG = os.path.join(ASSETS_PATH,"cutout1.png")
DARK_IMG = os.path.join(ASSETS_PATH,"cutout2.png")

# Sound
PLAYER_SOUND = os.path.join(ASSETS_PATH,"receipt-printer-01-43872.mp3")
PHONE_SOUND = os.path.join(ASSETS_PATH,"synth-telephone-ring-001-8434.mp3")
ENEMY_TALK = os.path.join(ASSETS_PATH,"muffled-talking-6161.mp3")
AMBIANCE_SOUND = os.path.join(ASSETS_PATH, 'menschenmenge-142716.mp3')
# Dialogue texts
START_DIALOGUE = os.path.join(ASSETS_PATH,"start_text.txt")
DIALOGUE_TWO = os.path.join(ASSETS_PATH,"dialogue_two.txt")
DIALOGUE_THREE = os.path.join(ASSETS_PATH,"dialogue_three.txt")
FINAL_DIALOGUE = os.path.join(ASSETS_PATH,"final_text.txt")

# Maps
MAP_ONE = os.path.join(ASSETS_PATH,"map1.txt")
MAP_TWO = os.path.join(ASSETS_PATH,"map2.txt")
MAP_THREE = os.path.join(ASSETS_PATH,"map3.txt")

# Credits
CREDITS_TEXT = os.path.join(ASSETS_PATH,"credits_text.txt")
RBG_TEXT = os.path.join(ASSETS_PATH,"robo_bakers.txt")
CREDITS_IMG = os.path.join(ASSETS_PATH,"creditspic.jpg")