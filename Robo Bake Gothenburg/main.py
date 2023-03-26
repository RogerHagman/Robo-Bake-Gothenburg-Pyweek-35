import pygame
"""Robo Bake Gothenburg Unnamed Game"""

class Game():
    """
    defining game variables 
    """
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('RoboBake Studios')
        self.tile_size = 50
        
        
        
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

    def __init__(self,lvl:int):
        """_summary_

        Args:
            lvl (int): specifies which map to load
        """
        Game.__init__(self)
        self.tile_list = []
        self.wall_list = []
        # load images
        wall_img = pygame.image.load("assets/wall.png")

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
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.wall_list.append(tile)
                col_count += 1
            row_count += 1
    def fetch_data(self,lvl:int):
        worlds = {
            1:
            [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
            [1, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 7, 1, 1, 1, 0, 0, 2, 2, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 7, 0, 5, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1], 
            [1, 0, 1, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
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

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            pygame.draw.rect(self.screen, (255, 255, 255), tile[1], 2)

class Dialogues():
    """ """