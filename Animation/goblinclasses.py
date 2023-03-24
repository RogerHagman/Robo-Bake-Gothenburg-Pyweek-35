from pygame import sprite, image, transform, surface

class Walker(sprite.Sprite):
    """
    Sprite that walks
    """
    walkL = []   # List of images to animate walking left
    walkR = []

    isJump = False
    jumpCount = 10

    left = False    # Currently facing/walking left
    right = False
    walkCount = 0

    def __init__(self, pos, img, imgcode='', steps=9, width=40, height=60, vel=5, lim=852, timer=27) -> None:
        super().__init__(   )

        # Starting position, tuple of coordinates
        self.x = pos[0]
        self.y = pos[1]
        
        #Load images
        #Images for walking animation should be named "L1"+imgcode / "R1"+imgcode
        self.img = image.load(img)
        self.steps = steps
        for step in range(steps):
            l = 'L' + str(step+1) + imgcode + '.png'
            self.walkL.append(image.load(l))
            r = 'R' + str(step+1) + imgcode + '.png'
            self.walkR.append(image.load(r))
        
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
        
        return step, self.x, self.y
    
    def jump(self):
        if not(self.isJump):
            self.isJump = True
            self.right = False
            self.left = False
            self.walkCount = 0
    
class Still(sprite.Sprite):

    def __init__(self, pos, img, size) -> None:
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.img = transform.scale(image.load(img), (size))
    
    def draw(self):
        return self.img, self.x, self.y
    
class StatusArea():

    statuses = {}
    # Each displayable status is a tuple
    # First element a unique string

    def __init__(self, size, axis, font, color = (255,255,255)) -> None:
        self.area = surface.Surface((size))
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
        
