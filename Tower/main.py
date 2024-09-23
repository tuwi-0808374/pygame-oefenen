import pygame
import constants as c

# init
pygame.init()

# create clock
clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Game")

# game loop
run = True
while run:

    clock.tick(c.FPS)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
