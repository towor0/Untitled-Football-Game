import pygame
from player import Player
from camera import Camera
from football import Football
from npc import Goalie


# Controls the game
class Controller:
    # create all instances
    def __init__(self):
        self.objs = {
            "player": Player(400, 1100),
            "ball": Football(400, 1000),
            "goalie": Goalie(400, 60)
        }
        self.camera = Camera()
        self.background = pygame.image.load("assets/field.png").convert_alpha()

    # reset game
    def reset(self):
        self.objs = {
            "player": Player(400, 1100),
            "ball": Football(400, 1000),
            "goalie": Goalie(400, 60)
        }

    # update all instances
    def update(self, dt):
        self.objs["player"].update(dt, self.objs["ball"])
        self.objs["ball"].update(dt)
        if self.objs["ball"].goal:
            self.camera.shake()
            self.reset()
        self.objs["goalie"].update(dt, self.objs["ball"])
        self.camera.update(dt, self.objs["player"].pos)

    # draw all instances
    def draw(self, window):
        window.blit(self.background, (-self.camera.rect.x, -self.camera.rect.y))
        for key in sorted(self.objs.keys(), key=lambda a: self.objs[a].rect.bottom):
            self.objs[key].draw(window, self.camera.rect)
