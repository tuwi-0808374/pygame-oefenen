from math import trunc

import pygame
from sys import exit
from random import randint, choice

pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PYGAME LESSEN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('assets/audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.gravity = 0
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            # Fly
            fly_frame_1 = pygame.image.load('assets/graphics/Fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('assets/graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            # Snail
            snail_frame_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(screen_width + 50, screen_width + 250), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {int(current_time / 1000)}", False, 'black')
    score_rect = score_surf.get_rect(center = (screen_width / 2, 20))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return False
    else:
        return True

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/Ground.png').convert()

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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(type = choice(['fly', 'snail', 'snail', 'snail'])))

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

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        screen.blit(game_name, game_name_rect)
        obstacle_group.empty()

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            score_message = test_font.render(f"Score: {int(score / 1000)}", False, 'black')
            score_message_rect = score_message.get_rect(center=(screen_width / 2, screen_height - 50))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)