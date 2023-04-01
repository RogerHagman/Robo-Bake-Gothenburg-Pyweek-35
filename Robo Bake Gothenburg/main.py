import pygame
import time
from settings import *
from sprites import *
from scenes import *
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

        self.player.set_love(love)
        
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

game = Game()
game.run()