import pygame
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

        player_image = pygame.image.load(PLAYER_IMG)
        player_image = pygame.transform.scale_by(player_image, TILESIZE/player_image.get_height())
        self.player = Player(5,5, player_image)

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
            clock.tick(FPS)

        if start_menu.started() == False:
            pygame.quit()

        dialogue_one = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, START_DIALOGUE)
        while dialogue_one.run_level():
            self.screen.blit(dialogue_one.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        love, accepted = dialogue_one.get_state()
        if not accepted:
            pygame.quit()

        #Add "love" to Player
        
        level_one = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_ONE, self.player)
        while level_one.run_level():
            self.screen.blit(level_one.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()
            pygame.quit()
        elif exited:
            self.player.set_player_state(True,False,False)
        else:
            pygame.quit()

        level_two = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_TWO, self.player)
        while level_two.run_level():
            self.screen.blit(level_two.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()
            pygame.quit()
        elif exited:
            self.player.set_player_state(True,False,False)
        else:
            pygame.quit()

        level_three = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_THREE, self.player)
        while level_three.run_level():
            self.screen.blit(level_three.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()
            pygame.quit()        
        elif exited:
            won = True
        else:
            pygame.quit()

        if won:
            final_dialogue = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, FINAL_DIALOGUE)
            while final_dialogue.run_level():
                self.screen.blit(final_dialogue.render_level(), (0,0))
                pygame.display.update()
                clock.tick(FPS)

        pygame.quit()
    
    def game_over(self):
        final_text = "They caught me... oh no!"
        final_printer_statement = pygame.font.Font(SCENE_FONT, SCENE_FONT_LARGE).render(final_text ,True, PRINTER_COLOR)
        self.screen.fill(BLACK)
        self.screen.blit(final_printer_statement, (SCREEN_WIDTH/2 - final_printer_statement.get_width()/2, 200))
        time.sleep(5)
        
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

    def __init__(self, width: int, height: int, lvl:str, player) -> None:
        super().__init__(width, height)
        self.level_width = width*0.8

        self.bg = pygame.transform.scale(pygame.image.load(BG_IMG),(self.level_width,height))
        self.map = Map(lvl, height)

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

        self.player.update((self.width, self.heigth), self.walls, self.doors)
        self.enemies.update((self.width,self.heigth))
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
        self.font_small = pygame.font.Font(SCENE_FONT, SCENE_FONT_SMALL)
        self.font_large = pygame.font.Font(SCENE_FONT, SCENE_FONT_LARGE)
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
        pos = pygame.mouse.get_pos()                #Change color when hovering over text
        if self.start_button.collidepoint(pos):
            self.surface.blit(self.start_button_s, (SCREEN_WIDTH/2 - self.start_button_s.get_width()/2, 200))
        else:
            self.surface.blit(self.start_button_u, (SCREEN_WIDTH/2 - self.start_button_u.get_width()/2, 200))
        if self.quit_button.collidepoint(pos):
            self.surface.blit(self.quit_button_s, (SCREEN_WIDTH/2 - self.start_button_s.get_width()/2, 250))
        else:
            self.surface.blit(self.quit_button_u, (SCREEN_WIDTH/2 - self.start_button_u.get_width()/2, 250))
        return self.surface

    def started(self):
        return self.start

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
        pie_img = pygame.transform.scale(pygame.image.load(PIE_IMG),(self.tile_size,self.tile_size))#6
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
                #    pie = Pie(x=x, y=y, figure=pie_img)
                #    self.pie_list.append(pie)
                if tile == 7:                           # 7 = plant 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    plant = Clutter(x=x, y=y, figure=img)
                #    self.clutter_list.append(plant)
                if tile == 8:                           # 8 = phone 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    phone = Distraction(x=x, y=y, figure=img)
                #    self.distractions_list.append(phone)
                if tile == 9:                           # 9 = desk 
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                #    phone = Distraction(x=x, y=y, figure=img)
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

    def keep_aspect_ratio(self, img):
        """
        Returns image scaled to tile size, maintaining aspect ratio
        NP: the pygame.transform.scale_by() function is experimental
        """
        biggest_side = max(img.get_width(), img.get_height())
        return pygame.transform.scale_by(img, self.tile_size/biggest_side)

class Dialogue(Level):
    """
    Loads a text file and creates a dialogue scene
    """

    def __init__(self, width, height, text_file:str) -> None:
        super().__init__(width, height)
        self.font_small = pygame.font.Font(SCENE_FONT,SCENE_FONT_SMALL)
        self.font_medium = pygame.font.Font(SCENE_FONT, SCENE_FONT_MEDIUM)
        self.font_large = pygame.font.Font(SCENE_FONT, SCENE_FONT_LARGE)
        self.option_rects = []
        self.selection_color = []
        self.diadict = {}
        self.turn = 1
        self.love = 0       # How much more or less Printo will like you at the end of this dialogue
        self.accepted = True

        with open(text_file) as f:
            contents = f.read()
        found = re.findall(r'(?:\$)([^\$]+)' , contents, re.MULTILINE)      #Parsing the text
        for section in found:
            id = int(re.match(r'([0-9]*)', section).group())
            printer_says = re.match(r'(?:[0-9]*)(.+)', section).groups(1)[0]
            turn = DialogueOptions(id, printer_says)
            options = re.findall(r'(?:\*)(.+)', section)
            for opt in options:
                # Pattern splits in to list like:
                # ["You poor thing, are you alright? Wait, aren't you our office printer?", '4', '+', '']
                turn.add_option(re.split(r'(?:\#)([0-9]+)([-+@])?', opt))
            
            self.diadict[id] = turn


    def render_level(self) -> pygame.surface.Surface:            
        self.surface.fill(BLACK)
        turn = self.diadict[self.turn]          #Get the DialogueOptions object of current turn

        printer_string = turn.get_printer()
        rect = pygame.rect.Rect(50,50, self.width-100, self.heigth-100)
        self.wrap_text(printer_string, PRINTER_COLOR, rect, self.font_large)

        self.option_rects = []                  #Keep track of where we blit the text, so we can click on it
        for n, option in enumerate(turn.get_options()):
            rect = pygame.rect.Rect(50,100*(n+3), self.width-100, self.heigth-100)
            _, y = self.wrap_text(option[0], self.selection_color[n-1], rect, self.font_medium)
            rect.update(50, 100*(n+3), self.width-100, y)
            self.option_rects.append(rect)
        
        self.surface.blit(self.font_small.render('Press space to skip', True, WHITE), (self.width//2, self.heigth-50))
        
        #for rect in self.option_rects:
        #    pygame.draw.rect(self.surface, GREEN, rect, 2)
        return self.surface
    
    
    def run_level(self) -> bool:
        turn = self.diadict[self.turn]

        options = turn.get_options()
        self.selection_color = []
        for n in range(len(options)):
            self.selection_color.append(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                for n,textbutton in enumerate(self.option_rects):
                    if textbutton.collidepoint(click):
                        self.turn = int(options[n][1])      # What the next Turn will be
                        match options[n][2]:                # Option makes Printo likes you more/less
                            case None:
                                pass
                            case '-':
                                self.love -=1
                            case '+':
                                self.love +=1
                            case '@':
                                self.accepted = False

            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_SPACE:
                    self.run = False
        
        pos = pygame.mouse.get_pos()                        
        for n,textbutton in enumerate(self.option_rects):
            if textbutton.collidepoint(pos):                    # Change color when hovering over text
                self.selection_color[n-1] = DIALOGUE_CHOICE
            else:
                self.selection_color[n-1] = WHITE

        if self.diadict[self.turn].get_printer() == 'END':
            self.run = False
        return self.run
    
    def get_state(self):
        return self.love, self.accepted

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
        self.printer_says = p   # One string
        self.options = []       # List of tuples (string: what the player says, int: the turn this choice will lead to)
    
    def add_option(self, option):
        self.options.append(option)
    
    def get_printer(self):
        return self.printer_says
    
    def get_options(self):
        return self.options

game = Game()
game.run()