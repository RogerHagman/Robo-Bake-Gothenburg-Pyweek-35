import pygame
import os
import sys
import random
import re
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """ 
    Initialize display and player.
    defining game variables 
    """
    def __init__(self):

        self.screen_width = 800
        self.screen_height = 800

        #Gets the relative path to the Assets folder
        assets_path = os.path.join(sys.path[0], 'Assets')
        self.bg = pygame.image.load(os.path.join(assets_path, 'bg.png'))

        pimg = pygame.image.load(os.path.join(assets_path, 'player.png'))
        pimg = pygame.transform.scale(pimg, (30,30))
        self.player = Player(0,0, pimg)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('RoboBake Studios')
        self.tile_size = 40
    
    def run(self):
        """
        Runs each screen/level in turn.
        Control framerate with clock.
        """
        pygame.init()

        clock = pygame.time.Clock()

        start_menu = Menu(self.screen_width, self.screen_height)
        while start_menu.run_level():
            self.screen.blit(start_menu.render_level(), (0,0))
            pygame.display.update()
            clock.tick(30)

        level_one = TelephoneRoom(self.screen_width, self.screen_height, 1, self.player)
        while level_one.run_level():
            self.screen.blit(level_one.render_level(), (0,0))
            pygame.display.update()
            clock.tick(30)
        
        alive, exited, won = self.player.get_player_state()
        if exited:
            level_two = TelephoneRoom(self.screen_width, self.screen_height, 2, self.player)
            while level_two.run_level():
                self.screen.blit(level_two.render_level(), (0,0))
                pygame.display.update()
                clock.tick(30)
        

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

        self.map = Map(lvl=lvl, tile_size=50)

        self.walls = pygame.sprite.Group(self.map.get_walls())
        self.doors = pygame.sprite.Group(self.map.get_doors())
        self.clutter = pygame.sprite.Group(self.map.get_clutter())
        self.distractions = pygame.sprite.Group(self.map.get_distractions())
        self.enemies = pygame.sprite.Group(self.map.get_enemies())
        self.pies = pygame.sprite.Group(self.map.get_pies())

        start_pos = self.map.get_player()
        self.player = player
        self.player.set_start_position(start_pos)

    def render_level(self) -> pygame.surface.Surface:
        self.surface.blit(self.map, (0,0))

        for wall in self.walls:
            self.surface.blit(wall.get_figure_shape(), wall.get_position())
        for door in self.doors:
            self.surface.blit(door.get_figure_shape(), door.get_position())
        for clutter in self.clutter:
            self.surface.blit(clutter.get_figure_shape(), clutter.get_position())
        for dist in self.distractions:
            self.surface.blit(dist.get_figure_shape(), dist.get_position())
        for enemy in self.enemies:
            self.surface.blit(enemy.get_figure_shape(), enemy.get_position())


        return self.surface
    
    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                self.player.update(keys, (self.width, self.heigth))
        
        self.enemies.update()

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

        self.font = pygame.font.SysFont('arial', 40)
        self.surface.fill((0,0,0))
        self.title = self.font.render('Robo Bake Gothenburg', True, (255, 255, 255))
        start_button = self.font.render('Start', True, (255, 255, 255))
        quit_button = self.font.render('Quit', True, (255, 255, 255))
        pie_button = self.font.render('Pie recipes', True, (255, 255, 255))

        self.surface.blit(self.title, (width/2 - self.title.get_width()/2, 50))
        
        self.start_button = self.surface.blit(start_button, (width/2 - start_button.get_width()/2, 200))
        self.quit_button = self.surface.blit(quit_button, (width/2 - quit_button.get_width()/2, 250 ))
        self.pie_button = self.surface.blit(pie_button, (width/2 - pie_button.get_width()/2, 300))

    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if self.start_button.collidepoint(click):
                    self.run = False
                elif self.quit_button.collidepoint(click):
                    self.run = False
                    pygame.quit()
                elif self.pie_button.collidepoint(click):
                    print("Mmmm pie")
                    self.run = False
                    pygame.quit()
        return self.run
    
    def render_level(self) -> pygame.surface.Surface:

        return self.surface


class GameObject(pygame.sprite.Sprite):
    """ A superclass for all game objects, extends pygame.sprite.Sprite. """
    def __init__(self, x, y, figure):
        """
        params: 
        @x - horizontal position
        @y - vertical position
        figure - figure object (like image or shape)
        """
        super().__init__()
        self.figure = figure
        # I think this should with something like tile_size
        self.surf = pygame.Surface((figure.get_width(), figure.get_height()))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.x, self.y = x, y

    def update(self):
        """Update the object's state each frame."""
        pass
    
    def draw(self, screen):
        """Draw an object on the screen."""
        screen.blit(self.figure, (self.x, self.y))

    def get_position(self):
        """Get the object's position as a tuple of (x, y) screen coordinates."""
        return self.x, self.y
    
    def set_position(self, x, y):
        self.x, self.y = x, y

    def get_figure_shape(self):
        """Get the object's figure object."""
        return self.figure

class Player(GameObject):
    """A class for the main character."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.speed = 5
        # This flips to False if player exits a level/finishes the game or gets hit by an enemy.
        self.is_alive = True
        self.is_exited = False
        self.is_win = False
    def update(self, pressed_keys, screen_dimensions):
        """Update the player's position based on key presses and the game's state."""
        delta_x, delta_y = 0, 0

        if pressed_keys[pygame.K_UP] and self.y > 0:
            delta_y = -1

        elif pressed_keys[pygame.K_DOWN] and self.y < screen_dimensions[1] - 1:
            delta_y = 1

        elif pressed_keys[pygame.K_LEFT] and self.x > 0:
            delta_x = -1

        elif pressed_keys[pygame.K_RIGHT] and self.x < screen_dimensions[0] - 1:
            delta_x = 1

        # Update the player's position based on the delta values and speed.

        # OLD CODE
        # old_x, old_y = self.get_position()
        # future_x, future_y= self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)
        # self.set_position((old_x + future_x),(old_y + future_y))

        old_x, old_y = self.get_position()
        future_x, future_y= (delta_x * self.speed, delta_y * self.speed)
        self.set_position((old_x + future_x),(old_y + future_y))

    def get_player_state(self):
        """
        Returns a tuple of player states
        params:     @is_alive: bool, 
                    @is_exited: bool,
                    @is_win: bool
        """
        return self.is_alive, self.is_exited, self.is_win

    def set_player_state(self, is_alive, is_exited, is_win):
        """Accepts a tuple of player states"""
        self.is_alive = is_alive
        self.is_exited = is_exited
        self.is_win = is_win

    def collision(self, other):
        if isinstance(other, Wall):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            self.rect.topleft = pos_before_col
            # Set the player's speed to 0
            self.speed = 0

        elif isinstance(other, Door):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            # Player Exits the current Map if it is the last door, the player wins. 
            # If it is not game continues on next level
            if Door.get_last_door():
                self.set_player_state = (True, True, True)
            else:
                self.set_player_state = (True, True, False)
        elif isinstance(other, Enemy):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            # Player dies and looses the game
            self.set_player_state = (False, True, False)

class Enemy(GameObject):
    """A class for Moving Enemy Characters"""
    def __init__(self, x, y,figure):
        super().__init__(x, y, figure)
        self.direction = (0, 0)
        self.speed = 3
    def update(self, screen_dimensions):
        # Generates a random direction, with extra copies of the current direction
        directions = [self.direction] * 10 + [(1, 0), (-1, 0), (0, 1), (0, -1)]
        delta_x, delta_y = random.choice(directions)
        
        # Updates the current direction
        self.direction = (delta_x, delta_y)

        new_x, new_y = self.x + delta_x, self.y + delta_y

        # Checks if the new position is a valid one
        if 0 <= new_x < screen_dimensions[0]and 0 <= new_y < screen_dimensions[1]:
            # Update the position of the enemy

            self.x, self.y = new_x, new_y

            self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)
 
class Wall(GameObject):
    """A class for wall objects."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        x = self.x
        y = self.y
        self.is_windowed = False
    def update(self, x,y):
        self.x = x
        self.y = y

    def set_windowed(self, window):
        self.is_windowed = window

    def get_windowed(self):
        return self.is_windowed

class Door(GameObject):
    """Class for defining exit points on the Map."""
    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        x = self.x
        y = self.y
        
    def set_last_door(self, last_door):
        self.is_last_door = last_door

    def get_last_door(self):
        return self.get_last_door
    
    def update(self):
        pass


class Hud(GameObject):
    """ """
    pass
class Map(Game): 

    def __init__(self,lvl:int, tile_size):
        """_summary_
        Args:
            lvl (int): specifies which map to load, 
            tile_size(int): tile_size from Game
        """
        self.tile_size = tile_size
        self.wall_list = []
        self.door_list = []
        self.player = None
        self.enemy_list = []
        self.pie_list = []
        self.clutter_list = []
        self.distractions_list = []
        
        # load images
        wall_img = pygame.image.load("Assets/wall.png") #1
        player_img = pygame.image.load("Assets/player.png")#2
        door_img = pygame.image.load("Assets/door.png")#3
        enemy_img = pygame.image.load("Assets/enemy.png")#4
        pie_img = pygame.image.load("Assets/pie.png")#5
        plant_img = pygame.image.load("Assets/plant.png")#6
        phone_img = pygame.image.load("Assets/phone.png")#7
        data = self.fetch_data(lvl)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    wall = Wall(x=img_rect.x, y= img_rect.y, figure=img)
                    self.wall_list.append(wall)
                if tile == 2:
                    img = pygame.transform.scale(player_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    player = Player(x=img_rect.x, y= img_rect.y, figure=img)
                    self.player = player
                if tile == 3:
                    img = pygame.transform.scale(door_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    door = Door(x=img_rect.x, y= img_rect.y, figure=img)
                    self.door_list.append(door)
                if tile == 4:
                    img = pygame.transform.scale(enemy_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    enemy = Enemy(x=img_rect.x, y= img_rect.y, figure=img)
                    self.door_list.append(enemy)
                if tile == 5:
                    img = pygame.transform.scale(pie_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    pie = Pie(x=img_rect.x, y= img_rect.y, figure=img)
                    self.door_list.append(pie)
                if tile == 6:
                    img = pygame.transform.scale(plant_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    plant = Clutter(x=img_rect.x, y= img_rect.y, figure=img)
                    self.clutter_list.append(plant)
                if tile == 7:
                    img = pygame.transform.scale(phone_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    phone = Distraction(x=img_rect.x, y= img_rect.y, figure=img)
                    self.door_list.append(phone)
                
                col_count += 1
                
            row_count += 1
    # getters for object lists
    def get_player(self):
        return self.player.get_position()
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
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 6, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 5, 0, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [3, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        }
        return worlds[lvl]


class Dialogue(Level):
    """
    Loads a text file and creates a dialogue scene
    """

    def __init__(self, width, height, text_file) -> None:
        super().__init__(width, height)
        self.font = pygame.font.SysFont('arial', 40)
        self.option_rects = []
        self.diadict = {}
        self.turn = 1

        with open(text_file) as f:
            contents = f.read()
        found = re.findall(r'(?:\$)([^\$]+)' , contents, re.MULTILINE)
        for section in found:
            id = int(re.match(r'([0-9]*)', section).group())
            printer_says = re.match(r'(?:[0-9]*)(.+)', section).groups(1)[0]
            
            turn = DialogueOptions(id, printer_says)

            options = re.findall(r'(?:\*)(.+)', section)
            for opt in options:
                turn.add_option(re.split(r'(?:\#)', opt))
            
            self.diadict[id] = turn


    def render_level(self) -> pygame.surface.Surface:            
        self.surface.fill((0,0,0))
        turn = self.diadict[self.turn]
        printer_says = self.font.render(turn.get_printer(), True, (255, 255, 255))
        self.surface.blit(printer_says, (self.width/2 - printer_says.get_width()/2, 100))

        self.option_rects = []
        for n, option in enumerate(turn.get_options()):
            text = self.font.render(option[0], True, (255, 255, 255))
            self.option_rects.append(self.surface.blit(text, (self.width/2 - text.get_width()/2, 100*(n+3))))
        
        return self.surface
    
    
    def run_level(self) -> bool:
        turn = self.diadict[self.turn]
        if turn.get_printer() == 'END':
            self.run = False

        options = turn.get_options()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                for n,textbutton in enumerate(self.option_rects):
                    if textbutton.collidepoint(click):
                        self.turn = int(options[n][1])


        return super().run_level()

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

