import pygame

class Walker(pygame.sprite.Sprite):
    """
    Sprite that walks
    """
    def __init__(self, pos, img, imgcode='', steps=9, width=40, height=60, vel=5, lim=852, timer=27) -> None:
        super().__init__()
        self.walkL = []   # List of images to animate walking left
        self.walkR = []

        self.isJump = False
        self.jumpCount = 10

        self.left = False    # Currently facing/walking left
        self.right = False
        self.walkCount = 0

        self.take = False   #Only Goblin class uses these currently
        self.punch = False
        self.rtake = None
        self.ltake = None
        self.rpunch = None
        self.lpunch = None
        self.downtime = None

        # Starting position, tuple of coordinates
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, width, height)
        
        #Load images
        #Images for walking animation should be named "L1"+imgcode / "R1"+imgcode
        self.img = pygame.image.load(img)
        self.steps = steps
        for step in range(steps):
            l = 'L' + str(step+1) + imgcode + '.png'
            self.walkL.append(pygame.image.load(l))
            r = 'R' + str(step+1) + imgcode + '.png'
            self.walkR.append(pygame.image.load(r))
        
        #Controls the walking
        self.width = width
        self.height = height
        self.vel = vel
        self.timer = timer

        #Width of the screen
        self.lim = lim

    def walkLeft(self):
        if self.x>self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
    
    def walkRight(self):
        if self.x < self.lim - self.vel - self.width:
            self.x += self.vel
            self.left = False
            self.right = True
    
    def stand(self):
        self.left = False
        self.right = False
        self.walkCount = 0
    
    def update(self, time=None):
        """
        Returns the current image for the walking animation.
        Including if the character is standing still or jumping.
        """
        if self.isJump:
            if self.jumpCount >= -10:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: 
                self.jumpCount = 10
                self.isJump = False

        if self.walkCount +1 >= self.timer:
            self.walkCount = 0
        
        if self.take:                           #Take/punch done standing still
            if self.left:
                step=self.ltake
            else:
                step=self.rtake
            if self.downtime == None:
                self.downtime = 1000
            elif self.downtime >0:
                self.downtime -= time
            else:
                self.downtime = None
                self.take = False

        elif self.punch:
            if self.left:
                step = self.lpunch
            else:
                step = self.rpunch
            if self.downtime == None:
                self.downtime = 1000
            elif self.downtime >0:
                self.downtime -= time
            else:
                self.downtime = None
                self.punch = False

        elif self.left:
            step = self.walkL[self.walkCount//3]
            self.walkCount +=1
        elif self.right:
            step = self.walkR[self.walkCount//3]
            self.walkCount +=1
        else:
            step = self.img
        
        #Rect is what is needed for sprite's built in collision methods, important to update!
        self.rect.update(self.x, self.y, self.width, self.height)
        
        return step, self.x, self.y
    
    def jump(self):
        if not(self.isJump):
            self.isJump = True
            self.right = False
            self.left = False
            self.walkCount = 0

    def get_x(self):
        return self.x
    
    def isBusy(self):
        if self.take or self.punch:
            return True

class Hero(Walker):
    health = 5
    apples = 0
    goblins_fed = 0
    damage_downtime = 0

    def __init__(self, pos, img) -> None:
        super().__init__(pos=pos, img=img)

    def pick_up_apple(self):
        self.apples+=1

    def be_eaten(self, time:int):
        if self.damage_downtime == 0:
            self.damage_downtime = 1000
            self.health -=1
            self.health = max(0, self.health)
        else:
            self.damage_downtime -= time
            self.damage_downtime = max(0, self.damage_downtime)
    
    def feed_goblin(self):
        self.apples -= 1
    
    def update(self):
        return super().update()
    
    def walkLeft(self):
        super().walkLeft()

    def walkRight(self):
        super().walkRight()

    def jump(self):
        super().jump()
    
    def get_health(self):
        return ('Health', self.health)
    
    def get_apples(self):
        return ('Apples', self.apples)
        
    def get_goblins(self):
        return ('Goblins Fed', self.goblins_fed)

    def get_x(self):
        return super().get_x()

class Goblin(Walker):

    hungry = True
    downtime = 0

    def __init__(self, pos, img, take:int, punch:int, imgcode='E') -> None:
        super().__init__(pos=pos, img=img, imgcode=imgcode)
        
        self.rtake=(pygame.image.load('R' + str(take) + imgcode + '.png'))
        self.ltake=(pygame.image.load('L' + str(take) + imgcode + '.png'))
        self.rpunch=(pygame.image.load('R' + str(punch) + imgcode + '.png'))
        self.lpunch=(pygame.image.load('L' + str(punch) + imgcode + '.png'))

        self.left = True
    
    def update(self, time):
        return super().update(time)
    
    def walkLeft(self):
        super().walkLeft()

    def walkRight(self):
        super().walkRight()
    
    def attack(self):
        self.punch = True
    
    def accept(self):
        self.take = True
        self.hungry = False
        self.left = False
        self.right = False
    
    def isHungry(self):
        return self.hungry

    def get_x(self):
        return super().get_x()

class Still(pygame.sprite.Sprite):
    def __init__(self, pos, img, size) -> None:
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.img = pygame.transform.scale(pygame.image.load(img), (size))
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])
    
    def update(self):
        return self.img, self.x, self.y
    
class StatusArea():

    statuses = {}
    # Each displayable status is a tuple
    # First element a unique string

    def __init__(self, size, axis, font, color = (255,255,255)) -> None:
        self.area = pygame.surface.Surface((size))
        self.color = color
        self.size = size
        if axis == 0:
            self.dim = size[0] -10  #Just some padding
        elif axis == 1:
            self.dim = size[1] -10
        else: raise ValueError('Axis must be 0 or 1')
        self.axis = axis
        self.font = font
    
    def update(self, status):
        self.statuses[status[0]] = status[1]
    
    def draw(self):
        """
        Draws all statuses onto self, evenly spaced,
        horizontally or vertically based on axis.
        """
        #For now, this will just render text for each status
        #The idea is to expand with options to draw bars or objects.
        self.area.fill(self.color)

        if len(self.statuses)>0:
            spacing = self.dim/len(self.statuses)
            for n, status in enumerate(self.statuses):
                text = status + ' : ' + str(self.statuses[status])
                caption = self.font.render(text, 1, (0,0,0))
                if self.axis == 0:
                    center = (self.size[1] - self.font.size(caption)[1])//2
                    self.area.blit(caption, ((n*spacing)+10, center))
                else: 
                    center = (self.size[0] - self.font.size(text)[0])//2
                    self.area.blit(caption, (center, (n*spacing)+10))

        return self.area
        
class FeedTheGoblins():
    """
    Main game class
    """
    def __init__(self, bg) -> None:
        self.win = pygame.display.set_mode((1002,480))
        pygame.display.set_caption("Feed the Goblins")
        self.bg = pygame.image.load(bg)

        self.sb = StatusArea(size=(150,480), axis=1, font=pygame.font.SysFont('Arial', (20)))
        self.apples = pygame.sprite.Group()
        self.goblins = pygame.sprite.Group()

        apple = Still(pos=(20,400), img='apple.png', size=(25,25))
        self.apples.add(apple)

        goblin = Goblin(pos=(400, 350), img='L1E.png', take=10, punch=11)
        self.goblins.add(goblin)

        self.hero = Hero(pos=(150,350),img='standing.png')

        self.sb.update(self.hero.get_health())
        self.sb.update(self.hero.get_apples())

        self.clock = pygame.time.Clock()


    def redrawGameWindow(self):
        """
        Draws window, and all sprites
        """
        self.win.blit(self.bg, (0,0))
        self.win.blit(self.sb.draw(), (852,0))

        step, x, y = self.hero.update()
        self.win.blit(step, (x,y))

        for goblin in self.goblins:
            if goblin.isHungry() and not goblin.isBusy():
                if self.hero.get_x()<goblin.get_x():
                    goblin.walkLeft()
                else:
                    goblin.walkRight()
            step, x, y = goblin.update(self.clock.get_time())
            self.win.blit(step, (x,y))

        for apple in self.apples:
            img, x, y = apple.update()
            self.win.blit(img, (x,y))

        pygame.display.update() 
    
    def run_game(self):

        run = True

        while run:
            self.clock.tick(27)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.hero.walkLeft()
            elif keys[pygame.K_RIGHT]:
                self.hero.walkRight()    
            else:
                self.hero.stand()
            if keys[pygame.K_SPACE]:
                self.hero.jump()

            #Collisions
            apple = pygame.sprite.spritecollideany(self.hero, self.apples)
            if apple != None:
                self.hero.pick_up_apple()
                self.apples.remove(apple)
                self.sb.update(self.hero.get_apples())
            
            goblin = pygame.sprite.spritecollideany(self.hero, self.goblins)
            if goblin !=None and goblin.isHungry():
                if self.hero.get_apples()[1]>0:
                    self.hero.feed_goblin()
                    self.sb.update(self.hero.get_apples())
                    goblin.accept()
                else:
                    self.hero.be_eaten(self.clock.get_time())
                    self.sb.update(self.hero.get_health())
                    goblin.attack()

            self.redrawGameWindow() 
