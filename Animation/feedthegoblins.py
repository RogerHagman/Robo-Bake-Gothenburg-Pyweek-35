"""
In Feed the Goblins, you must pick up apples and feed them to the goblins chasing you.
If a goblin catches you and you have no apples, they will start to eat you.
You automatically pick up apples by touching them. 
How many apples you have will be shown in the side bar.
We will start with one apple on the ground and one goblin. 
"""

import pygame

from goblinclasses import FeedTheGoblins

pygame.init()

game = FeedTheGoblins('bg.jpg')

game.run_game()

pygame.quit()