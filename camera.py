import pygame
import random


# tracks player's y position and adjust the camera position accordingly
class Camera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 800, 600)
        self.targety = 0
        self.shaketime = 0

    def shake(self):
        self.shaketime = 60

    def update(self, dt, player):
        # camera smoothening
        self.targety = player.y
        self.rect.centery += (self.targety - self.rect.centery)/10
        # camera limitations
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 700:
            self.rect.y = 700
        # apply camera shakes
        if self.shaketime > 0:
            self.shaketime -= dt
            self.rect.x = random.randint(-4, 4)
            self.rect.y += random.randint(-4, 4)
        else:
            self.rect.x = 0


