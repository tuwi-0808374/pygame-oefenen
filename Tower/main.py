import pygame
import constants as c
import json
from enemy import Enemy
from world import World

# init
pygame.init()

# create clock
clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Game")

# load images
# Map
map_image = pygame.image.load("levels/level.png").convert_alpha()
# Enemies
enemy_image = pygame.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

# Load json data for level
with open('levels/level.tmj') as file:
    word_data = json.load(file)

# Create world
world = World(word_data, map_image)
world.process_data()

# create groups
enemy_group = pygame.sprite.Group()

waypoints = world.waypoints

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)


# game loop
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey")

    # draw level
    world.draw(screen)

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
