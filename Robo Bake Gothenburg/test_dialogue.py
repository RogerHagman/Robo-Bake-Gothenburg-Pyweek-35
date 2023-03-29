import pygame

import main

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

dialogue = main.Dialogue(800,800, 'Assets/test_text.txt')
while dialogue.run_level():
    screen.blit(dialogue.render_level(), (0,0))
    pygame.display.update()
    clock.tick(30)
pygame.quit()