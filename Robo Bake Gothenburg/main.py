import pygame
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """ """

    """
    defining game variables 
    """
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg = pygame.image.load('Assets/bg.png')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('RoboBake Studios')
        self.tile_size = 40
    
    def run(self):
        pygame.init()
        run = True
        while run:
            self.screen.blit(self.bg,(0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            pygame.display.update()
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
    An office space with telephones
    """

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

        new_map = Map(1)                        # Does Map need more parameters in init?

        self.map_objects = new_map.fetch_Data()

        self.office_workers = None              # Office workers in different locations and with movement patterns
        self.player = Player(0,0, None)

    def render_level(self) -> pygame.surface.Surface:
        self.surface.blit(self.map, (0,0))

        for thing in self.map_objects:
            self.surface.blit(thing[0], thing[1])

        for worker in self.office_workers:
            self.surface.blit(worker.get_surface(), worker.get_pos())

        return self.surface
    
    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.walkLeft()
        elif keys[pygame.K_RIGHT]:
            self.player.walkRight()    
        else:
            self.player.stand()
        if keys[pygame.K_SPACE]:
                self.player.interact()
        
        thing = pygame.sprite.spritecollideany(self.player, self.map_objects)
        if thing != None:
            #We collided with something
            pass
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
                    print("There's no level to start yet")
                    self.run = False
                elif self.quit_button.collidepoint(click):
                    print("This quit button works as intended")
                    self.run = False
                elif self.pie_button.collidepoint(click):
                    print("Mmmm pie")
                    self.run = False
        return self.run
    
    def render_level(self) -> pygame.surface.Surface:

        return self.surface


class GameObject(pygame.sprite.Sprite):
    """ A superclass for all game objects, extends pygame.sprite.Sprite. """
    def __init__(self, x, y, figure):
        """

        @params: 
        x - horizontal position
        y - vertical position
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

    def get_figure_shape(self):
        """Get the object's figure object."""
        return self.figure

class Player(GameObject):
    """A class for the main character."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        self.speed = 5

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
        self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)

    def collision(self, other):
        if isinstance(other, Wall):
            # Gets the position of the player before the collision happend. And moves the player back.
            pos_before_col = self.get_position()
            self.rect.topleft = pos_before_col
            # Set the player's speed to 0
            self.speed = 0

class Wall(GameObject):
    """A class for wall objects."""

    def __init__(self, x, y, figure):
        super().__init__(x, y, figure)
        x = self.x
        y = self.y

    def update(self, x,y):
        self.x = x
        self.y = y

    def get_position(self):
        """returns the walls position as (x, y) screen coordinates."""
        return self.x, self.y

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
                    self.enemy_list.append(enemy)
                if tile == 5:
                    img = pygame.transform.scale(pie_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    pie = Pie(x=img_rect.x, y= img_rect.y, figure=img)
                    self.pie_list.append(pie)
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
                    self.distractions_list.append(phone)
                
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


class Dialogues():
    """ """
    pass


