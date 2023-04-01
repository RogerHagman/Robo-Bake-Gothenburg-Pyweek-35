import pygame
import re
from settings import *
from sprites import *
from level_components import *

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
        self.hud = Hud((width*0.2, height))

        self.walls = pygame.sprite.Group(self.map.get_walls())
        self.doors = pygame.sprite.Group(self.map.get_doors())
        self.clutter = pygame.sprite.Group(self.map.get_clutter())
        self.distractions = pygame.sprite.Group(self.map.get_distractions())
        self.enemies = pygame.sprite.Group(self.map.get_enemies())
        self.pies = pygame.sprite.Group(self.map.get_pies())

        start_pos = self.map.get_player_pos()
        self.player = player
        self.player.set_position(start_pos[0], start_pos[1])

        self.immobile_sprites = pygame.sprite.Group(self.walls)
        self.immobile_sprites.add(self.doors)
        self.immobile_sprites.add(self.clutter)
        self.immobile_sprites.add(self.distractions)
        self.immobile_sprites.add(self.pies)

        self.surface.blit(self.bg, (0,0))
        for wall in self.walls:
            wall.draw(self.surface)
        self.fog = Fog(self.surface.copy())
        self.shadow = Shadow((self.level_width, height))

    def render_level(self) -> pygame.surface.Surface:
        # In order to get fog effect, first blit background
        self.surface.blit(self.bg,(0,0)) 
        # Next, all immobile sprites
        for sprite in self.immobile_sprites:
            sprite.draw(self.surface)
        # Next, the fog
        self.fog.draw(self.player.rect.copy(), self.surface)
        # Next, all enemies within visible distance (radius)       
        for enemy in self.enemies:                                      
            if pygame.sprite.collide_circle(enemy, self.player):
                enemy.draw(self.surface)
        # Finally, darkness
        self.shadow.draw(self.player.rect.copy(), self.surface)
        self.player.draw(self.surface)  

        self.surface.blit(self.hud.update(self.player.get_pie_love()), (self.level_width, 0))
        return self.surface
    
    def run_level(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        self.player.update((self.width, self.heigth), self.walls, self.doors, self.enemies)
        self.enemies.update((self.width,self.heigth), self.walls, self.distractions)

        pie = pygame.sprite.spritecollideany(self.player, self.pies)
        if pie != None and not pie.is_eaten():
            pie.eat()
            self.player.eat_pie()
            
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


class Dialogue(Level):
    """
    Loads a text file and creates a dialogue scene.

    Each "turn", with one statement from PRINTO3000,
    and multiple responses for the player to choose,
    is a DialogueTurn object contained in diadict.
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
            turn = DialogueTurn(id, printer_says)
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
                if event.key == pygame.K_SPACE:
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
