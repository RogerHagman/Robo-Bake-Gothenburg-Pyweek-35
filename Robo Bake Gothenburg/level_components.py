import pygame
from sprites import *


class Map(): 

    def __init__(self,lvl:str, map_size):
        """_summary_
        Args:
            lvl (str): specifies which map to load, 
            map_size is set by screen height.
        """
        self.tile_size = map_size//20
        self.wall_list = []
        self.door_list = []
        self.player = None
        self.enemy_list = []
        self.pie_list = []
        self.clutter_list = []
        self.distractions_list = []
        self.player_pos = (0,0)
        
        # Load images
        # Plant and desks are not the same height and width
        # If in doubt, use 'keep aspect ratio'
        wall_img = pygame.transform.scale(pygame.image.load(WALL_IMG),(self.tile_size,self.tile_size))#1
        door_img = pygame.transform.scale(pygame.image.load(DOOR_IMG),(self.tile_size,self.tile_size))#3
        enemy1_img = pygame.transform.scale(pygame.image.load(ENEMY1_IMG),(self.tile_size,self.tile_size))#4
        enemy2_img = pygame.transform.scale(pygame.image.load(ENEMY2_IMG),(self.tile_size,self.tile_size))#5
        pie_img = pygame.transform.scale(pygame.image.load(PIE_IMG),(self.tile_size*0.8,self.tile_size*0.8))#6
        plant_img = self.keep_aspect_ratio(pygame.image.load(PLANT_IMG))
        phone_img = pygame.transform.scale(pygame.image.load(PHONE_IMG),(self.tile_size,self.tile_size))#8
        desk_img = self.keep_aspect_ratio(pygame.image.load(DESK_IMG))#9

        with open(lvl) as file:
            map = file.read().splitlines()
        
        row_count = 0
        for row in map:
            col_count = 0
            for tile in row:
                if tile != '.':
                    tile = int(tile)
                if tile == 1:                           # 1 = wall 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    wall = Wall(x=x, y=y, figure=wall_img)
                    self.wall_list.append(wall)
                if tile == 2:                           # 2 = player 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    self.player_pos = (x,y)
                if tile == 3:                           # 3 = door 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    door = Door(x=x, y=y, figure=door_img)
                    self.door_list.append(door)
                if tile == 4:                           # 4 = enemy1 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    enemy1 = Enemy(x=x, y=y, figure=enemy1_img)
                    self.enemy_list.append(enemy1)
                if tile == 5:                           # 5 = enemy2 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    enemy2 = Enemy(x=x, y=y, figure=enemy2_img)
                    self.enemy_list.append(enemy2)
                if tile == 6:                           # 6 = pie 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    pie = Pie(x=x, y=y, figure=pie_img)
                    self.pie_list.append(pie)
                if tile == 7:                           # 7 = plant 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    plant = Clutter(x=x, y=y, figure=plant_img)
                    self.clutter_list.append(plant)
                if tile == 8:                           # 8 = phone 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    phone = Distraction(x=x, y=y, figure=phone_img)
                    self.distractions_list.append(phone)
                if tile == 9:                           # 9 = desk 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    desk = Clutter(x=x, y=y, figure=desk_img)
                    self.clutter_list.append(desk)
                col_count += 1
                
            row_count += 1
    # getters for object lists
    def get_player_pos(self):
        return self.player_pos
    def get_walls(self):
        return self.wall_list
    def get_doors(self):
        return self.door_list
    def get_enemies(self):
        return self.enemy_list
    def get_pies(self):
        return self.pie_list
    def get_clutter(self):
        return self.clutter_list
    def get_distractions(self):
        return self.distractions_list

    @staticmethod
    def keep_aspect_ratio(img, resize = 1):
        """
        Returns image scaled to tile size, maintaining aspect ratio
        NP: the pygame.transform.scale_by() function is experimental
        """
        biggest_side = max(img.get_width(), img.get_height()) 
        return pygame.transform.scale_by(img, (TILESIZE/biggest_side)*resize)
    
class DialogueTurn():

    def __init__(self, id:int, p:str) -> None:
        """
        A DialogueTurn has an id, what PRINTO3000 says,
        what the player can choose to respond,
        and what the response will lead to.
        Every DialogueTurn is added to the Dialogue class's
        'diadict' dictionary. 

        NB: DialogueOption's "id" is not currently being used,
        but it will correspond to its key in Dialogue's diadict.
        """
        self.id = id
        self.printer_says = p   # One string
        self.options = []       # List of list of strings
    
    def add_option(self, option):
        """
        The player's choices in a dialogue.
        Each option is a list with the following format:
        ['This is the text', 'X', 'Y'], where X is the id
        of the next DialogueTurn that will be selected,
        and 'Y' an optional special character. 
        """
        self.options.append(option)
    
    def get_printer(self):
        return self.printer_says
    
    def get_options(self):
        return self.options

class Hud():

    def __init__(self, size) -> None:
        self.surface = pygame.surface.Surface(size)
    
    def update(self, pie_love):
        self.surface.fill(LIGHTGREY)
        
        return self.surface

class Fog(pygame.sprite.Sprite):
    def __init__(self, size) -> None:
        super().__init__()
        self.rect = pygame.Rect(0,0,size[0], size[1])
        self.surface = pygame.Surface(size)
        self.surface = self.surface.convert_alpha()
        #self.visible_area = self.surface.copy()

        self.cutout = pygame.transform.scale(pygame.image.load(FOG_IMG), (TILESIZE*6,TILESIZE*6))

    def update(self, sprite_rect):
        self.surface.fill(BLACK)
        self.surface.set_alpha(200)
        x = sprite_rect.x + (sprite_rect.width//2)
        y = sprite_rect.y + (sprite_rect.height//2)
        
        self.surface.blit(self.cutout, (x -(TILESIZE*3), y-(TILESIZE*3)), self.surface.get_rect(), pygame.BLEND_RGBA_MULT)

        return self.surface