import math

import pygame
import constants as c

class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pygame.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 1500
        self.last_shot = pygame.time.get_ticks()
        self.selected = False
        self.target = None

        # position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        # calculate center coordinates
        self.x = (self.tile_x + .5) * c.TILE_SIZE
        self.y = (self.tile_y + .5 ) * c.TILE_SIZE

        # animation variables
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


    def load_images(self):
        # extract images from spritesheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group):
        if self.target:
            self.play_animation()
        else:
            if pygame.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist**2 + y_dist**2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        # check if enough time is passed since last update
        if pygame.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            self.last_shot = pygame.time.get_ticks()
            self.target = None

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)
        screen.blit(self.image, self.rect)