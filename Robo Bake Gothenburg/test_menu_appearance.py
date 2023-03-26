from main import Menu, TelephoneRoom

import pygame

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 500))
clock.tick(10)
start_menu = Menu(500, 500)

while start_menu.run_level():
    screen.blit(start_menu.render_level(), (0,0))
    clock.tick(10)
    pygame.display.update()

level_one = TelephoneRoom()
while level_one.run_level():
    screen.blit(level_one.render_level(), (0,0))
    pygame.display.update()

pygame.quit()