"""
In Feed the Goblins, you must pick up apples and feed them to the goblins chasing you.
If a goblin catches you and you have no apples, they will start to eat you.
You automatically pick up apples by touching them. 
How many apples you have will be shown in the side bar.
We will start with one apple on the ground and one goblin. 
"""

import pygame

import goblinclasses

pygame.init()

win = pygame.display.set_mode((1002,480))
pygame.display.set_caption("Feed the Goblins")
bg = pygame.image.load('bg.jpg')

sb = goblinclasses.StatusArea(size=(150,480), axis=1, font=pygame.font.SysFont('Arial', (20)))
sb.update(('Health', 5))
sb.update(('Apples', 0))
sb.update(('Wins', 'YES'))

apple = goblinclasses.Still((20,400), 'apple.png', (25,25))

hero = goblinclasses.Walker((150,350),'standing.png')

goblin = goblinclasses.Walker((400, 350), 'L1E.png', 'E')

clock = pygame.time.Clock()

def redrawGameWindow(window, walkers, stills):
    """
    Draws window, and all sprites
    """
    
    window.blit(bg, (0,0))
    window.blit(sb.draw(), (852,0))

    for sprite in walkers:
        step, x, y = sprite.walk()
        window.blit(step, (x,y))

    for sprite in stills:
        img, x, y = sprite.draw()
        window.blit(img, (x,y))

    pygame.display.update() 

run = True

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hero.walkLeft()
    elif keys[pygame.K_RIGHT]:
        hero.walkRight()    
    else:
        hero.stand()
    if keys[pygame.K_SPACE]:
        hero.jump()

    redrawGameWindow(win, [hero, goblin], [apple]) 
    
pygame.quit()