import pygame
import sys
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
        player_image = pygame.transform.scale_by(player_image, (TILESIZE*0.8)/player_image.get_height())
        self.player = Player(5,5, player_image)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
    
    def run(self):
        """
        Runs each screen/level in turn.
        Control framerate with clock.
        """
        pygame.init()
        exit_text = "Press any key to exit"
        self.exit_text = pygame.font.Font(SCENE_FONT, SCENE_FONT_SMALL).render(exit_text, True, WHITE)

        clock = pygame.time.Clock()

        start_menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        while start_menu.run_level():
            self.screen.blit(start_menu.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)

        if start_menu.started() == False:
            pygame.quit()
            sys.exit()

        dialogue_one = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, START_DIALOGUE)
        while dialogue_one.run_level():
            self.screen.blit(dialogue_one.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        love, accepted = dialogue_one.get_state()
        if not accepted:
            pygame.quit()
            sys.exit()
        self.player.set_love((love//2)+3)   #Base starting value is 3, up to +2 or -2 from dialogue
        
        level_one = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_ONE, self.player)
        while level_one.run_level():
            self.screen.blit(level_one.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()
        elif exited:
            self.player.set_player_state(True,False,False)
        else:
            pygame.quit()

        dialogue_two = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, DIALOGUE_TWO)
        while dialogue_two.run_level():
            self.screen.blit(dialogue_two.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        love, accepted = dialogue_two.get_state()
        self.player.set_love(max(love,0))

        level_two = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_TWO, self.player)
        while level_two.run_level():
            self.screen.blit(level_two.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()
        elif exited:
            self.player.set_player_state(True,False,False)
        else:
            pygame.quit()
            sys.exit()
        
        dialogue_three = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, DIALOGUE_THREE)
        while dialogue_three.run_level():
            self.screen.blit(dialogue_three.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        love, accepted = dialogue_three.get_state()
        self.player.set_love(max(love,0))

        level_three = TelephoneRoom(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_THREE, self.player)
        while level_three.run_level():
            self.screen.blit(level_three.render_level(), (0,0))
            pygame.display.update()
            clock.tick(FPS)
        alive, exited, won = self.player.get_player_state()
        if not alive:
            self.game_over()     
        elif exited:
            won = True
        else:
            pygame.quit()
            sys.exit()

        if won:
            final_dialogue = Dialogue(SCREEN_WIDTH, SCREEN_HEIGHT, FINAL_DIALOGUE)
            while final_dialogue.run_level():
                self.screen.blit(final_dialogue.render_level(), (0,0))
                pygame.display.update()
                clock.tick(FPS)
        
        # Credits
        caption_font = pygame.font.Font(SCENE_FONT, SCENE_FONT_LARGE)
        credits_font = pygame.font.Font(SCENE_FONT, SCENE_FONT_SMALL)
        cred_img = pygame.image.load(CREDITS_IMG)
        with open(RBG_TEXT) as file:
            rbglines = file.read().splitlines()
        with open(CREDITS_TEXT) as file:
            credlines = file.read().splitlines()
        column_one = (SCREEN_WIDTH/2)/2
        column_two = (SCREEN_WIDTH/2)+column_one
        self.screen.fill(BLACK)
        caption = caption_font.render('CREDITS', True, WHITE)
        self.screen.blit(caption, (SCREEN_WIDTH/2 - caption.get_width()/2, TILESIZE))

        for n, line in enumerate(rbglines):
            cred_line = credits_font.render(line, True, WHITE)
            self.screen.blit(cred_line, (column_one - cred_line.get_width()/2, TILESIZE*(n+3)))
        self.screen.blit(cred_img, (column_one - cred_img.get_width()/2, TILESIZE*8))

        for n, line in enumerate(credlines):
            cred_line = credits_font.render(line, True, WHITE)
            self.screen.blit(cred_line, (column_two - cred_line.get_width()/2, TILESIZE*(n+3)))
        self.screen.blit(self.exit_text, (SCREEN_WIDTH/2-self.exit_text.get_width()/2, SCREEN_HEIGHT-TILESIZE))
        pygame.display.update()
        #/Credits
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_LEFT\
                    or event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                    pass
                else:
                    pygame.quit()
                    sys.exit()
    
    def game_over(self):
        final_text = "They caught me... oh no!"
        final_printer_statement = pygame.font.Font(SCENE_FONT, SCENE_FONT_LARGE).render(final_text ,True, PRINTER_COLOR)
        self.screen.fill(BLACK)
        self.screen.blit(final_printer_statement, (SCREEN_WIDTH/2 - final_printer_statement.get_width()/2, TILESIZE*4))
        self.screen.blit(self.exit_text, (SCREEN_WIDTH/2-self.exit_text.get_width()/2, SCREEN_HEIGHT-TILESIZE))
        pygame.display.update()
        
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_LEFT\
                    or event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                    pass
                else:
                    pygame.quit()
                    sys.exit()

game = Game()
game.run()