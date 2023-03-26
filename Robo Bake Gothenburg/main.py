import pygame
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """ """
    pass

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
        new_map = Map(width, height)            # Does Map need more parameters in init?
        self.map = Map.draw()                   # What's this method really called? Are we getting a surface or array?

        self.map_objects = pygame.sprite.Group(Map.get_stuff())

        self.office_workers = None              # Office workers in different locations and with movement patterns
        self.player = Player()                  # Needs what in init?

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
    """ """
    pass
class Player(GameObject):
    """ """
    pass
class Hud(GameObject):
    """ """
    pass
class Map():
    """ """
    pass

class Dialogues():
    """ """