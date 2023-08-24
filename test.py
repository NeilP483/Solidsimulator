import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
draw_radius = 5
original_speed = 0
dt = 1/20.0
m = 1.00
strength = 50

def create_circle():
    width = screen.get_width()
    height = screen.get_height()
    pos = [width * random.random(), height * random.random()]
    theta = 2 * math.pi * random.random()
    vel = [original_speed * math.sin(theta), original_speed * math.cos(theta)]
    charge = random.random() > 0.5
    return [pos, vel, charge]

def draw_circle(circle):
    pygame.draw.circle(screen, ((0, 0, 255) if circle[2] else (255, 0, 0)), tuple(circle[0]), draw_radius)

def update_circle(circle):
    pos = circle[0]
    vel = circle[1]
    pos[0] += vel[0] * dt
    pos[1] += vel[1] * dt
    if(pos[0] < 0 or pos[0] >= screen.get_width()):
        vel[0] *= -1
        pos[0] = 0 if pos[0] < 0 else screen.get_width() - 1
    if(pos[1] < 0 or pos[1] >= screen.get_height()):
        vel[1] *= -1
        pos[1] = 0 if pos[1] < 0 else screen.get_height() - 1
def collide_circle(c1, c2):
    charge_1 = 1 if c1[2] else -1
    pos_1 = c1[0]
    pos_2 = c2[0]
    charge_2 = 1 if c2[2] else -1
    r = math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
    if r < draw_radius/2.0:
        return
    #rep_f = 2 * draw_radius / r / r / r + 1 / r / r
    rep_f = strength * (2 * draw_radius / r / r / r - 1 / r / r)
    rep_x = (pos_1[0] - pos_2[0]) / r * rep_f / m
    rep_y = (pos_1[1] - pos_2[1]) / r * rep_f / m
    c1[1][0] += rep_x * dt
    c2[1][0] -= rep_x * dt
    c1[1][1] += rep_y * dt
    c2[1][1] -= rep_y * dt
circles = [create_circle() for _ in range(50)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    for circle in circles:
        draw_circle(circle)
        update_circle(circle)
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                    collide_circle(circles[i], circles[j])
    # fill the screen with a color to wipe away anything from last frame

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()