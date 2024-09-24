import pygame
import constants as c
from enemy import Enemy

# init
pygame.init()

# create clock
clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Game")

# load images
enemy_image = pygame.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

# create groups
enemy_group = pygame.sprite.Group()

waypoints = [
    (100, 100),
    (400, 200),
    (400, 100),
    (200, 300),
]

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)


# game loop
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey")

    # draw enemy path
    pygame.draw.lines(screen, "red", False, waypoints)

    # update groups
    enemy_group.update()

    # draw groups
    enemy_group.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
