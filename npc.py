import pygame


class Goalie:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.sprite = {
            "front": pygame.image.load("assets/goalie_front.png").convert_alpha(),
            "right": pygame.image.load("assets/goalie_right.png").convert_alpha(),
            "left": pygame.image.load("assets/goalie_left.png").convert_alpha(),
            "fall_right": pygame.image.load("assets/goalie_fall_right.png").convert_alpha(),
            "fall_left": pygame.image.load("assets/goalie_fall_left.png").convert_alpha()
        }
        self.state = "front"
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.divepower = 5
        self.speed = 1.5
        self.jumpvel = pygame.Vector2(0, 0)
        self.fallcd = 30
        self.feet = pygame.Rect(0, 0, 12, 4)

    def update(self, dt, football):
        # movements
        vel = pygame.math.Vector2(0, 0)
        if self.state == "front":
            if football.possession == self:
                targetx = 400
                if targetx - self.pos.x > 0:
                    vel.x += self.speed * dt
                else:
                    vel.x -= self.speed * dt
                if abs(targetx - self.pos.x) < 2:
                    vel.x = 0
                    football.kick(25)
            else:
                if football.rect.centerx < 360:
                    targetx = 360
                elif football.rect.centerx > 440:
                    targetx = 440
                else:
                    targetx = football.rect.centerx
                if targetx - self.pos.x > 0:
                    vel.x += self.speed * dt
                else:
                    vel.x -= self.speed * dt
                if abs(targetx - self.pos.x) < 2:
                    vel.x = 0
                # dive
                if football.rect.centery < 100 and abs(football.rect.centerx - self.rect.centerx) > 8 and 360 <= football.rect.centerx <= 440:
                    if self.rect.centerx - football.rect.centerx > 0:
                        self.state = "left"
                        self.jumpvel = pygame.Vector2(-self.divepower, -1)
                    else:
                        self.state = "right"
                        self.jumpvel = pygame.Vector2(self.divepower, -1)
        elif self.state == "right" or self.state == "left":
            if self.jumpvel.y < 1:
                self.jumpvel.y += 0.1 * dt
                vel.x += self.jumpvel.x * dt
                vel.y += self.jumpvel.y * dt
            else:
                self.pos.y = 60
                if self.state == "right":
                    self.state = "fall_right"
                else:
                    self.state = "fall_left"
                self.fallcd = 30
        else:
            if self.fallcd > 0:
                self.fallcd -= dt
            else:
                self.state = "front"
        # saves
        if self.feet.colliderect(football.rect):
            football.getBall(self)
        self.pos.xy += vel
        self.rect.center = self.pos
        self.feet.centerx = self.pos.x
        self.feet.y = self.pos.y + 4

    def draw(self, window, camera):
        window.blit(self.sprite[self.state], (self.rect.x - camera.x, self.rect.y - camera.y))
