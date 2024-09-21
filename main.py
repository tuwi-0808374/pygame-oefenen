import pygame
from sys import exit
from random import randint

pygame.init()
screen_width = 800
screen_height = 400

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {int(current_time / 1000)}", False, 'black')
    score_rect = score_surf.get_rect(center = (screen_width / 2, 20))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        #list comprehension
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index > len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PYGAME LESSEN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

#obstacles
sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/Ground.png').convert()

obstacle_rect_list = []

# score_surf = test_font.render('gamers', False, 'Black')
# score_rect = score_surf.get_rect(center = (400, 50))

# Snail
snail_frame_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('assets/graphics/Fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('assets/graphics/Fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Player
player_walk_1 = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('PYGAME RUNNER', False, 'orange')
game_name = pygame.transform.rotozoom(game_name, 0, 2)
game_name_rect = game_name.get_rect(center = (screen_width/2, 60))

game_message = test_font.render('Press space to play', False, 'red')
game_message_rect = game_message.get_rect(center = (screen_width/2, screen_height - 50))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2) == 1:
                    obstacle_rect_list.append(
                        snail_surf.get_rect(bottomright=(randint(screen_width + 50, screen_width + 250), 300)))
                else:
                    obstacle_rect_list.append(
                        fly_surf.get_rect(bottomright=(randint(screen_width + 50, screen_width + 250), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        #block image transfer
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, 'Pink', score_rect)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            score_message = test_font.render(f"Score: {int(score / 1000)}", False, 'black')
            score_message_rect = score_message.get_rect(center=(screen_width / 2, screen_height - 50))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)