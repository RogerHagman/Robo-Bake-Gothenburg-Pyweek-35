import pygame

class Walker(pygame.sprite.Sprite):
    """
    Sprite that walks
    """
    def __init__(self, *groups, pos, img, imgcode='', steps=9, width=40, height=60, vel=5, lim=852, timer=27) -> None:
        super().__init__(*groups)
        self.walkL = []   # List of images to animate walking left
        self.walkR = []

        self.isJump = False
        self.jumpCount = 10

        self.left = False    # Currently facing/walking left
        self.right = False
        self.walkCount = 0

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
    
    def walk(self):
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
        if self.left:
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

class Hero(Walker):
    health = 5
    apples = 0
    goblins_fed = 0

    def __init__(self, pos, img) -> None:
        super().__init__(pos=pos, img=img)

    def pick_up_apple(self):
        self.apples+=1

    def be_eaten(self):
        self.health =-1
        self.health = max(0, self.health)
    
    def walk(self):
        return super().walk()
    
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

class Still(pygame.sprite.Sprite):
    def __init__(self, *groups, pos, img, size) -> None:
        super().__init__(*groups)
        self.x = pos[0]
        self.y = pos[1]
        self.img = pygame.transform.scale(pygame.image.load(img), (size))
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])
    
    def draw(self):
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

    #def add(self, status):
    #    self.statuses.append(status)
    
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

        goblin = Walker(pos=(400, 350), img='L1E.png', imgcode='E')
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

        step, x, y = self.hero.walk()
        self.win.blit(step, (x,y))

        for sprite in self.goblins:
            step, x, y = sprite.walk()
            self.win.blit(step, (x,y))

        for sprite in self.apples:
            img, x, y = sprite.draw()
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
            if goblin !=None:
                if self.hero.get_apples()[1]>0:
                    pass
                else:
                    self.hero.be_eaten()
                    self.sb.update(self.hero.get_health())


            self.redrawGameWindow() 

