import pygame
import time
from controller import Controller

# initiate pygame
pygame.init()
# clock and previous time for delta time calculation
clock = pygame.time.Clock()
prev_time = time.time()

# define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# create pygame window and instance initiation
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
controller = Controller()
running = True


# game loop
while running:
    # 60 frames cap
    clock.tick(60)
    # allows for frame independence
    now = time.time()
    dt = (now - prev_time) * 60
    prev_time = now
    # check if the player wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update all instances
    controller.update(dt)
    # draw all instances
    controller.draw(window)
    pygame.display.flip()
# quit pygame
pygame.quit()
