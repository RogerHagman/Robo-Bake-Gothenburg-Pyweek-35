import pygame
import os
import sys
import random
import time
import re
from settings import *
from sprites import *
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """ 
    Initialize display and player.
    defining game variables 
    """
    def __init__(self):

        self.player = Player(5,5)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
    
    def run(self):
        """
        Runs each screen/level in turn.
        Control framerate with clock.
        """
        pygame.init()

        clock = pygame.time.Clock()

        start_menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        while start_menu.run_level():
            self.screen.blit(start_menu.render_level(), (0,0))
            pygame.display.update()
            clock.tick(30)

        if start_menu.start():
            level_one = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, 1, self.player)
            while level_one.run_level():
                self.screen.blit(level_one.render_level(), (0,0))
                pygame.display.update()
                clock.tick(30)
        
            alive, exited, won = self.player.get_player_state()

            if exited:
                final_text = "You won! Thank you for helping me!"
            else:
                final_text = "They caught me... oh no!"
            final_printer_statement = pygame.font.SysFont(SCENE_FONT, SCENE_FONT_LARGE).render(final_text ,1, PRINTER_COLOR)
            self.screen.fill(BLACK)
            self.screen.blit(final_printer_statement, (SCREEN_WIDTH/2 - final_printer_statement.get_width()/2, 200))

            time.sleep(5)
        pygame.quit()
            
        
class Level():
    """ 
    Base class for level design.
    
    Because the Game class has control over our pygame.display,
    any Level class needs a way to return its Surface to the Game.
    """
    def __init__(self, width:int, height:int) -> None:
        """
        Initialize surface, game objects and states
        """
        self.run = True
        self.width = width
        self.heigth = height
        self.surface = pygame.surface.Surface((width, height))

    def render_level(self) -> pygame.surface.Surface:
        """
        Blit game objects onto level surface and returns surface
        """
        #Blit
        #Blit
        return self.surface

    def run_level(self) -> bool:
        """
        Handles events and returns bool for Game to know the level is still running
        """

        #pygame events
        #collisions
        return self.run
        
class TelephoneRoom(Level):
    """
    An office space with telephones and nasty enemies
    """

    def __init__(self, width: int, height: int, lvl:int, player) -> None:
        super().__init__(width, height)
        self.level_width = width*0.8

        self.bg = pygame.transform.scale(pygame.image.load(BG_IMG),(self.level_width,height))
        self.map = Map(lvl, (self.level_width,height))

        self.walls = pygame.sprite.Group(self.map.get_walls())
        self.doors = pygame.sprite.Group(self.map.get_doors())
        self.clutter = pygame.sprite.Group(self.map.get_clutter())
        self.distractions = pygame.sprite.Group(self.map.get_distractions())
        self.enemies = pygame.sprite.Group(self.map.get_enemies())
        self.pies = pygame.sprite.Group(self.map.get_pies())

        start_pos = self.map.get_player_pos()
        self.player = player
        self.player.set_position(start_pos[0], start_pos[1])

        self.all_sprites = pygame.sprite.Group(self.walls)
        self.all_sprites.add(self.doors)
        self.all_sprites.add(self.clutter)
        self.all_sprites.add(self.distractions)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.pies)
        self.all_sprites.add(self.player)


    def render_level(self) -> pygame.surface.Surface:
        self.surface.blit(self.bg,(0,0))
        for sprite in self.all_sprites:
            sprite.draw(self.surface)

        return self.surface
    
    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False 

        self.player.update((self.width, self.heigth), self.all_sprites)
        
        self.enemies.update((self.width,self.heigth), self.all_sprites)

        alive, exited, _ = self.player.get_player_state()

        if not alive or exited:
            self.run = False
        
        return self.run
    
class Menu(Level):
    """
    Start Menu
    """
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.font_small = pygame.font.SysFont(SCENE_FONT, SCENE_FONT_SMALL)
        self.font_large = pygame.font.SysFont(SCENE_FONT, SCENE_FONT_LARGE)
        self.surface.fill(BLACK)
        self.title = self.font_large.render(TITLE, True, (WHITE))
        self.start_button_u = self.font_large.render('Start', True, (WHITE))
        self.start_button_s = self.font_large.render('Start', True, (DIALOGUE_CHOICE))
        self.quit_button_u = self.font_large.render('Quit', True, (WHITE))
        self.quit_button_s = self.font_large.render('Quit', True, (DIALOGUE_CHOICE))
        #pie_button = self.font_large.render('Pie recipes', True, (WHITE))

        self.surface.blit(self.title, (width/2 - self.title.get_width()/2, 50))
        
        self.start_button = self.surface.blit(self.start_button_u, (width/2 - self.start_button_u.get_width()/2, 200))
        self.quit_button = self.surface.blit(self.quit_button_u, (width/2 - self.quit_button_u.get_width()/2, 250 ))
        #self.pie_button = self.surface.blit(pie_button, (width/2 - pie_button.get_width()/2, 300))

        self.start = True

    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if self.start_button.collidepoint(click):
                    self.run = False
                elif self.quit_button.collidepoint(click):
                    self.run = False
                    self.start = False

        return self.run
    
    def render_level(self) -> pygame.surface.Surface:
        self.surface.fill(BLACK)
        self.surface.blit(self.title, (SCREEN_WIDTH/2 - self.title.get_width()/2, 50))
        pos = pygame.mouse.get_pos()
        if self.start_button.collidepoint(pos):
            self.surface.blit(self.start_button_s, (SCREEN_WIDTH/2 - self.start_button_s.get_width()/2, 200))
        else:
            self.surface.blit(self.start_button_u, (SCREEN_WIDTH/2 - self.start_button_u.get_width()/2, 200))
        if self.quit_button.collidepoint(pos):
            self.surface.blit(self.quit_button_s, (SCREEN_WIDTH/2 - self.start_button_s.get_width()/2, 250))
        else:
            self.surface.blit(self.quit_button_u, (SCREEN_WIDTH/2 - self.start_button_u.get_width()/2, 250))
        return self.surface

    def start(self):
        return self.start

class Map(Game): 

    def __init__(self,lvl:int, map_size:int):
        """_summary_
        Args:
            lvl (int): specifies which map to load, 
            tile_size(int): tile_size from Game
        """
        self.tile_size = map_size[0]//20
        self.wall_list = []
        self.door_list = []
        self.player = None
        self.enemy_list = []
        self.pie_list = []
        self.clutter_list = []
        self.distractions_list = []
        
        # Load images
        wall_img = pygame.image.load(WALL_IMG)#1
        #player_img = pygame.image.load(PLAYER_IMG)#2
        door_img = pygame.image.load(DOOR_IMG)#3
        enemy1_img = pygame.image.load(ENEMY1_IMG)#41
        enemy2_img = pygame.image.load(ENEMY2_IMG)#42
        pie_img = pygame.image.load(PIE_IMG)#5
        plant_img = pygame.image.load(PLANT_IMG)#6
        phone_img = pygame.image.load(PHONE_IMG)#7
        
        data = self.fetch_data(lvl)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    wall = Wall(x=x, y=y, figure=img)
                    self.wall_list.append(wall)
                if tile == 2:
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    self.player_pos = (x,y)
                if tile == 3:
                    img = pygame.transform.scale(door_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    door = Door(x=x, y=y, figure=img)
                    self.door_list.append(door)
                if tile == 41:
                    img = pygame.transform.scale(enemy1_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    enemy1 = Enemy(x=x, y=y, figure=img)
                    self.enemy_list.append(enemy1)
                if tile == 42:
                    img = pygame.transform.scale(enemy2_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    enemy2 = Enemy(x=x, y=y, figure=img)
                    self.enemy_list.append(enemy2)
                if tile == 5:
                    img = pygame.transform.scale(pie_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    pie = Pie(x=img_rect.x, y= img_rect.y, figure=img)
                #    self.pie_list.append(pie)
                if tile == 6:
                    img = pygame.transform.scale(plant_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    plant = Clutter(x=img_rect.x, y= img_rect.y, figure=img)
                #    self.clutter_list.append(plant)
                if tile == 7:
                    img = pygame.transform.scale(phone_img, (self.tile_size, self.tile_size))
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    phone = Distraction(x=img_rect.x, y= img_rect.y, figure=img)
                #    self.distractions_list.append(phone)
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
    
    def fetch_data(self,lvl:int):
        worlds = {
            1:
            [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 0, 7, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 5, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 6, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 5, 0, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 41, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [3, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],

        }
        return worlds[lvl]


class Dialogue(Level):
    """
    Loads a text file and creates a dialogue scene
    """

    def __init__(self, width, height, text_file) -> None:
        super().__init__(width, height)
        self.font_small = pygame.font.SysFont(SCENE_FONT, SCENE_FONT_SMALL)
        self.font_large = pygame.font.SysFont(SCENE_FONT, SCENE_FONT_LARGE)
        self.option_rects = []
        self.selection_color = []
        self.diadict = {}
        self.turn = 1

        with open(text_file) as f:
            contents = f.read()
        found = re.findall(r'(?:\$)([^\$]+)' , contents, re.MULTILINE)      #Parsing the text
        for section in found:
            id = int(re.match(r'([0-9]*)', section).group())
            printer_says = re.match(r'(?:[0-9]*)(.+)', section).groups(1)[0]
            
            turn = DialogueOptions(id, printer_says)

            options = re.findall(r'(?:\*)(.+)', section)
            for opt in options:
                turn.add_option(re.split(r'(?:\#)', opt))
            
            self.diadict[id] = turn


    def render_level(self) -> pygame.surface.Surface:            
        self.surface.fill(BLACK)
        turn = self.diadict[self.turn]          #Get the DialogueOptions object of current turn

        printer_string = turn.get_printer()
        rect = pygame.rect.Rect(50,100, self.width-100, self.heigth-100)
        self.wrap_text(printer_string, PRINTER_COLOR, rect, self.font_large)

        self.option_rects = []                  #Keep track of where we blit the text, so we can click on it
        for n, option in enumerate(turn.get_options()):
            rect = pygame.rect.Rect(50,100*(n+3), self.width-100, self.heigth-100)
            _, y = self.wrap_text(option[0], self.selection_color[n], rect, self.font_large)
            rect.update(50, 100*(n+3), self.width-100, y)
            self.option_rects.append(rect)
        
        self.surface.blit(self.font_small.render('Press space to skip', True, (WHITE) ), (self.width//2, self.heigth-50))

        return self.surface
    
    
    def run_level(self) -> bool:
        turn = self.diadict[self.turn]
        if turn.get_printer() == 'END':
            self.run = False

        options = turn.get_options()
        self.selection_color = []
        for n in range(len(options)):
            self.selection_color.append((WHITE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                for n,textbutton in enumerate(self.option_rects):
                    if textbutton.collidepoint(click):
                        self.turn = int(options[n][1])
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_SPACE:
                    self.run = False
            pos = pygame.mouse.get_pos()
            for n,textbutton in enumerate(self.option_rects):
                if textbutton.collidepoint(pos):
                    self.selection_color[n] = (DIALOGUE_CHOICE)

        return super().run_level()

    def wrap_text(self, text, color, rect, font, aa=True):
        """
        draw some text into an area of a surface
        automatically wraps words to width
        returns any text that didn't get blitted
        """
        y = rect.top
        lineSpacing = -5
        # get the height of the font
        fontHeight = font.size("Tg")[1]
        while text:
            i = 1
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1
            # render the line and blit it to the surface
            image = font.render(text[:i], aa, color)
            self.surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            # remove the text we just blitted
            text = text[i:]
        return text, y-rect.top

class DialogueOptions():

    def __init__(self, id, p) -> None:
        self.id = id
        self.printer_says = p
        self.options = []
    
    def add_option(self, option):
        self.options.append(option)
    
    def get_printer(self):
        return self.printer_says
    
    def get_options(self):
        return self.options

game = Game()
game.run()