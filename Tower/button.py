import pygame

class Button():
    def __init__(self, x, y, image, single_clicked):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_clicked

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()


        # check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True

                if self.single_click:
                    self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False


        # draw button on screen
        surface.blit(self.image, self.rect)

        return action