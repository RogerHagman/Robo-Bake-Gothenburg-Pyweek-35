import pygame
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """
    defining game variables 
    """
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 1000
        self.bg = pygame.image.load('Assets/bg.png')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('RoboBake Studios')
        self.tile_size = 50
    
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
    """ """
    pass
class Menu():
    """ """
    pass
class GameObject(pygame.sprite.Sprite):
    """ """
    pass
class Player(GameObject):
    """ """
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
        self.wall_list = [] # Wall object
        # load images
        wall_img = pygame.image.load("Assets/wall.png")

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
                    wall = Wall(x=img_rect.x, y= img_recty, figure=img)
                    self.wall_list.append(tile)
                col_count += 1
            row_count += 1
               
    def fetch_data(self,lvl:int):
        worlds = {
            1:
            [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 1, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1], 
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 1, 1, 1, 1], 
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        }
        return worlds[lvl]


class Dialogues():
    """ """
    

game = Game()
game.run()