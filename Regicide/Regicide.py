import pygame
import engine
import sys

#Some global variables
draw = pygame.image.load('images/BACK.png')
draw = pygame.transform.scale(draw, (int(238*0.6), int(332*0.6)))
discard = pygame.image.load('images/BACK.png')
discard = pygame.transform.scale(discard, (int(238*0.6), int(332*0.6)))
message = ''

def drawButton(screen, position, text):
    """
    Draws button, returns its rect
    """
    small_font = pygame.font.SysFont('comicsans', 30, True)
    text_render = small_font.render(text, 1, (0, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    """
    draw some text into an area of a surface
    automatically wraps words
    returns any text that didn't get blitted
    """
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text

def renderGame(window):
    """
    Renders image and text,
    Also contains event handling, because to click on drawn objects
    we need access their rects after they are drawn.
    """
    global game
    global run
    global message

    # Non-clickables
    big_font = pygame.font.SysFont('comicsans',60, True)
    small_font = pygame.font.SysFont('comicsans', 30, True)
    window.fill((15,0,169))
    window.blit(big_font.render(f'Health : {game.royal.get_health()}', 1, (0, 0, 0)), (100, 50))
    window.blit(big_font.render(f'Attack : {game.royal.get_attack()}', 1, (0, 0, 0)), (100, 100))
    text_rect = pygame.rect.Rect(50, 200, 300, 150)
    text_rect2 = pygame.rect.Rect(50, 350, 300, 150)    #For game alerts/messages
    drawText(window, game.get_royal_immunity(), (0,0,0), text_rect, small_font)
    drawText(window, message, (0,0,0), text_rect2, small_font)
    window.blit(game.royal.get_card().image, (400, 50))
    window.blit(draw, (700, 50))
    draw.blit(small_font.render('Draw', 1, (0,0,0)), (40,30))
    draw.blit(small_font.render(f'{game.draw_deck.length()}', 1, (0,0,0)), (40,60))
    window.blit(discard, (850, 50))
    discard.blit(small_font.render('Discard', 1, (0,0,0)), (30, 30))
    discard.blit(small_font.render(f'{game.discard_pile.length()}', 1, (0,0,0)), (40, 60))

    #Clickables
    button = drawButton(window, (450, 400), game.get_state())
    
    rendered_played = []    #Rects of played cards after drawing them
    rendered_hand = []      #Rects of cards in hand after drawing them
    for n, card in enumerate(game.get_played()):
        rendered_played.append(window.blit(card.image, (94*n, 450)))
    for n, card in enumerate(game.get_hand()):
        if card in game.get_selected():
            rendered_hand.append(window.blit(card.image, (128*n, 580)))
        else:
            rendered_hand.append(window.blit(card.image, (128*n, 600)))

    pygame.display.flip()


    #Event handling
    click = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = event.pos
            if button.collidepoint(click):
                match game.get_state():
                    case 'Charge':
                        if game.charge():
                            game.attack()
                            message = ''
                        else:
                            message = "Invalid card selection!"
                    case 'Discard':
                        if game.discard():
                            game.defend()
                        else:
                            message = "You must discard your opponent's full attack value!"
                    case 'Over':
                        pygame.quit()
                        sys.exit()
            else:
                for n, card in enumerate(game.get_hand()):
                    if rendered_hand[n].collidepoint(click):
                        game.select_card(card)
                        message = '' 
    return run

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Regicide solo")
game = engine.Engine()

run = True
while run:
    run = renderGame(window)
    pygame.display.update()