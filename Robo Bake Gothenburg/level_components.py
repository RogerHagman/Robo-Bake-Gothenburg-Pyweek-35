import pygame
from sprites import *


class Map(): 

    def __init__(self,lvl:str):
        """_summary_
        Args:
            lvl (str): specifies which map to load, 
            map_size is set by screen height.
        """
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
        wall_img = pygame.transform.scale(pygame.image.load(WALL_IMG),(TILESIZE, TILESIZE))#1
        door_img = pygame.transform.scale(pygame.image.load(DOOR_IMG),(TILESIZE,TILESIZE))#3
        enemy1_img = pygame.transform.scale(pygame.image.load(ENEMY1_IMG),(TILESIZE,TILESIZE))#4
        enemy2_img = pygame.transform.scale(pygame.image.load(ENEMY2_IMG),(TILESIZE,TILESIZE))#5
        pie_img = pygame.transform.scale(pygame.image.load(PIE_IMG),(TILESIZE*0.8,TILESIZE*0.8))#6
        plant_img = self.keep_aspect_ratio(pygame.image.load(PLANT_IMG))
        phone_img = pygame.transform.scale(pygame.image.load(PHONE_IMG),(TILESIZE,TILESIZE))#8
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
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    wall = Wall(x=x, y=y, figure=wall_img)
                    self.wall_list.append(wall)
                if tile == 2:                           # 2 = player 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    self.player_pos = (x,y)
                if tile == 3:                           # 3 = door 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    door = Door(x=x, y=y, figure=door_img)
                    self.door_list.append(door)
                if tile == 4:                           # 4 = enemy1 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    enemy1 = Enemy(x=x, y=y, figure=enemy1_img)
                    self.enemy_list.append(enemy1)
                if tile == 5:                           # 5 = enemy2 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    enemy2 = Enemy(x=x, y=y, figure=enemy2_img)
                    self.enemy_list.append(enemy2)
                if tile == 6:                           # 6 = pie 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    pie = Pie(x=x, y=y, figure=pie_img)
                    self.pie_list.append(pie)
                if tile == 7:                           # 7 = plant 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    plant = Clutter(x=x, y=y, figure=plant_img)
                    self.clutter_list.append(plant)
                if tile == 8:                           # 8 = phone 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
                    phone = Distraction(x=x, y=y, figure=phone_img)
                    self.distractions_list.append(phone)
                if tile == 9:                           # 9 = desk 
                    x = col_count * TILESIZE
                    y = row_count * TILESIZE
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
        self.width = size[0]
        self.height = size[1]
        self.pie_img = pygame.transform.scale(pygame.image.load(LONE_PIE_IMG), (TILESIZE,TILESIZE))
        self.heart_img = pygame.transform.scale(pygame.image.load(HEART_IMG), (TILESIZE,TILESIZE))
    
    def update(self, pie_love):
        self.surface.fill(LIGHTGREY)
        self.surface.fill(DARKGREY, (TILESIZE//2, TILESIZE//2, self.width-TILESIZE, self.height-TILESIZE))

        pies, love = pie_love

        row_count = 0
        for row in range(int(pies/3) + (pies%3>0)):             # Divide by 3 and round UP
            col_count = 0
            for n in range(3):
                if pies > 0:
                    pies -= 1
                    self.surface.blit(self.pie_img, (TILESIZE + (n*TILESIZE), TILESIZE + (TILESIZE*row)))
                col_count += 1
            row_count +=1
            if row_count > 11:
                break
        
        row_count = 0
        for row in range(int(love/3) + (love%3>0)):
            col_count = 0
            for n in range(3):
                if love > 0 :
                    love -= 1
                    self.surface.blit(self.heart_img, (TILESIZE+ (n*TILESIZE), TILESIZE*15 + (TILESIZE*row)))
                col_count += 1
            row_count += 1
        
        return self.surface


class Fog():
    def __init__(self, image) -> None:
        self.surface = image
        self.surface = self.surface.convert_alpha()
        self.cutout = pygame.transform.scale(pygame.image.load(FOG_IMG), (TILESIZE*4,TILESIZE*4))

    def draw(self, sprite_rect, screen):
        x = sprite_rect.x + (sprite_rect.width//2)
        y = sprite_rect.y + (sprite_rect.height//2)
        self.surface.blit(self.cutout, (x -(TILESIZE*2), y-(TILESIZE*2)), self.surface.get_rect(), pygame.BLEND_RGBA_MIN)
        screen.blit(self.surface, (0,0))

class Shadow():
    def __init__(self, size) -> None:
        self.surface = pygame.Surface(size)
        self.surface = self.surface.convert_alpha()
        self.cutout = pygame.transform.scale(pygame.image.load(DARK_IMG), (TILESIZE*6,TILESIZE*6))

    def draw(self, sprite_rect, screen):
        self.surface.fill(BLACK)
        self.surface.set_alpha(200)
        x = sprite_rect.x + (sprite_rect.width//2)
        y = sprite_rect.y + (sprite_rect.height//2)
        self.surface.blit(self.cutout, (x -(TILESIZE*3), y-(TILESIZE*3)), self.surface.get_rect(), pygame.BLEND_RGBA_MULT)
        screen.blit(self.surface, (0,0))
    
