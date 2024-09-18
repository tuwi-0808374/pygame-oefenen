from turtledemo.penrose import start

import pygame
from sys import exit

pygame.init()
screen_width = 800
screen_height = 400

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {int(current_time / 1000)}", False, 'black')
    score_rect = score_surf.get_rect(center = (screen_width / 2, 20))
    screen.blit(score_surf, score_rect)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PYGAME LESSEN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = True
start_time = 0

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/Ground.png').convert()

# score_surf = test_font.render('gamers', False, 'Black')
# score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    start_time = pygame.time.get_ticks()

    if game_active:
        #block image transfer
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, 'Pink', score_rect)
        # screen.blit(score_surf, score_rect)
        display_score()

        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = screen_width
        screen.blit(snail_surf, snail_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill("yellow")

    pygame.display.update()
    clock.tick(60)