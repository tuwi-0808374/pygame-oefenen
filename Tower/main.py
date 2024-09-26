import pygame
import constants as c
import json
from enemy import Enemy
from world import World
from turret import Turret

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
# Individual turret image for mouse cursor
cursor_turret = pygame.image.load("assets/images/turrets/cursor_turret.png").convert_alpha()
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
turret_group = pygame.sprite.Group()

waypoints = world.waypoints

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    # calculate sequential number of tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    # check if tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        # Check that there isn't already a turret
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        if space_is_free:
            turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(turret)

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
    turret_group.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # check if mouse is on game area
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    create_turret(mouse_pos)

    pygame.display.flip()

pygame.quit()
