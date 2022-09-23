import pygame
import math

# import all keys needed
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)


# player character
class Player:
    # player variables
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.sprite = {
            "front": pygame.image.load("assets/player_front.png").convert_alpha(),
            "back": pygame.image.load("assets/player_back.png").convert_alpha(),
            "left": pygame.image.load("assets/player_left.png").convert_alpha(),
            "right": pygame.image.load("assets/player_right.png").convert_alpha(),
        }
        self.facing = "front"
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = self.pos
        self.speed = 2
        self.feet = pygame.Rect(0, 0, 12, 4)
        self.powerKick = False
        self.kickPower = 0

    # update character
    def update(self, dt, football):
        # player movement
        vel = pygame.math.Vector2(0, 0)
        pressedKeys = pygame.key.get_pressed()
        # checks if player is moving diagonally
        if (pressedKeys[K_w] != pressedKeys[K_s]) and (pressedKeys[K_a] != pressedKeys[K_d]):
            if pressedKeys[K_w]:
                self.facing = "front"
                vel.y -= self.speed * (math.sqrt(2) / 2) * dt
            if pressedKeys[K_s]:
                self.facing = "back"
                vel.y += self.speed * (math.sqrt(2) / 2) * dt
            if pressedKeys[K_a]:
                vel.x -= self.speed * (math.sqrt(2) / 2) * dt
            if pressedKeys[K_d]:
                vel.x += self.speed * (math.sqrt(2) / 2) * dt
        else:
            if pressedKeys[K_w]:
                if not pressedKeys[K_s]:
                    self.facing = "front"
                vel.y -= self.speed * dt
            if pressedKeys[K_s]:
                if not pressedKeys[K_w]:
                    self.facing = "back"
                vel.y += self.speed * dt
            if pressedKeys[K_a]:
                if not pressedKeys[K_d]:
                    self.facing = "left"
                vel.x -= self.speed * dt
            if pressedKeys[K_d]:
                if not pressedKeys[K_a]:
                    self.facing = "right"
                vel.x += self.speed * dt
        # detects if it touches the ball
        if self.feet.colliderect(football.rect):
            football.getBall(self)
        # detects if player clicked any mouse buttons
        pressedMouse = pygame.mouse.get_pressed(3)
        if pressedMouse[0]:
            self.powerKick = True
            self.kickPower += 1 * dt
            if self.kickPower > 50:
                self.kickPower = 50
        elif self.powerKick:
            self.powerKick = False
            if football.possession == self:
                football.kick(self.kickPower)
            self.kickPower = 0
        # apply position changes
        self.pos.xy += vel.xy
        self.rect.center = self.pos
        self.feet.centerx = self.pos.x
        self.feet.y = self.pos.y + 4

    # display character
    def draw(self, window, camera):
        window.blit(self.sprite[self.facing], (self.rect.x - camera.x, self.rect.y - camera.y))
        if self.powerKick:
            powerRect = pygame.Rect(0, 0, self.kickPower / 50 * 16, 2)
            powerRect.x = self.rect.x - camera.x
            powerRect.y = self.rect.y - camera.y - 4
            pygame.draw.rect(window, (255, 255, 255), powerRect)
