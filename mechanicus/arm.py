import pygame
import math
import random

class Arm:
    COLOR = (0, 0, 255) # BLUE
    VEL = 2
    HEAD_RADIUS = 5
    ARM_WIDTH = 3
    MAX_RADIUS = 300

    def __init__(self):
        self.radius = random.uniform(0, 300)
        self.theta = random.uniform(0, 359)
        self.x, self.y = 100, 100
        self.time = 0
        self.max_time = 2000

    def draw(self, win, x0, y0):
        if self.theta > 359: self.theta = 0
        if self.theta < 0: self.theta = 359
        self.x, self.y = x0 + self.radius * math.cos(math.radians(self.theta)), y0 + self.radius * math.sin(math.radians(self.theta))
        pygame.draw.line(win, self.COLOR, (x0, y0), (self.x, self.y), self.ARM_WIDTH)
        pygame.draw.circle(win, (0, 255, 0), (self.x, self.y), self.HEAD_RADIUS)

    def rotate(self, clockwise=True):
        if clockwise:
            self.theta += self.VEL
        else:
            self.theta -= self.VEL

    def lengthen(self, lengthen):
        if lengthen:
            if self.radius < self.MAX_RADIUS:
                self.radius += self.VEL
        else:
            if self.radius > 0:
                self.radius -= self.VEL

    def reset(self, arm):
        self.theta[arm] = 0