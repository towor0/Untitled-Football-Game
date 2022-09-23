import pygame
from helper import *
import random


# football used during the game
class Football:
    # football variables
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.rect.center = self.pos
        self.possession = None
        self.sprite = pygame.image.load("assets/football.png").convert_alpha()
        self.kicked = False
        self.speed = [0, 0]
        self.kickAngle = 0
        self.screenpos = pygame.math.Vector2(0, 0)
        self.friction = root(60, 0.22)
        self.goal = False

    def kick(self, power, angle=0):
        if self.possession.__class__.__name__ == "Player":
            self.speed = angleSpeed(power/4, pygame.mouse.get_pos(), self.screenpos)
            self.possession = None
            self.kicked = True
        elif self.possession.__class__.__name__ == "Goalie":
            self.speed = angleSpeed(power/4, [random.randint(0, 800), 800], self.pos)
            self.possession = None
            self.kicked = True

    def getBall(self, character):
        if not self.possession.__class__.__name__ == "Goalie":
            self.possession = character

    # update football movements
    def update(self, dt):
        # movement based on character possession
        if self.possession.__class__.__name__ == "Player":
            self.pos.xy = self.possession.feet.center
            match self.possession.facing:
                case "front":
                    self.pos.y -= 4
                case "back":
                    self.pos.y += 4
                case "left":
                    self.pos.x -= 4
                case "right":
                    self.pos.x += 4
        elif self.possession.__class__.__name__ == "Goalie":
            self.pos.xy = self.possession.rect.center
            self.pos.y += 12
        # movement based on mouse position and power
        elif self.kicked:
            self.pos.xy += self.speed
            self.rect.center = self.pos.xy
            self.speed[0] *= self.friction
            self.speed[1] *= self.friction
            if -1 < self.speed[0] < 1 and -1 < self.speed[1] < 1:
                self.kicked = False
        # boarder detection
        if self.rect.left < 25:
            self.pos.x += 2
            self.speed[0] = -self.speed[0]
        if self.rect.right > 775:
            self.pos.x -= 2
            self.speed[0] = -self.speed[0]
        if self.rect.right < 444 and self.rect.left > 356 and self.rect.top < 50:
            if self.rect.right > 440:
                self.pos.x -= 2
                self.speed[0] = -self.speed[0]
            elif self.rect.left < 360:
                self.pos.x += 2
                self.speed[0] = -self.speed[0]
        elif self.rect.top < 50:
            self.pos.y += 2
            self.speed[1] = -self.speed[1]
        if self.rect.top > 1300:
            self.pos.y -= 2
            self.speed[1] = -self.speed[1]
        # goal detection
        if self.rect.bottom < 45 and self.rect.top > 18 and self.rect.right < 440 and self.rect.left > 360:
            self.speed[0] = 0
            self.speed[1] = 0
            self.goal = True
        self.rect.center = self.pos.xy

    def draw(self, window, camera):
        window.blit(self.sprite, (self.rect.x - camera.x, self.rect.y - camera.y))
        self.screenpos = [self.rect.centerx - camera.x, self.rect.centery - camera.y]
