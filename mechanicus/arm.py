import pygame
import math
import random

class Arm:
    COLOR = (0, 0, 255) # BLUE
    VEL = 2
    HINGE_RADIUS = 5
    ARM_WIDTH = 3
    ARM_LENGTH = 100

    def __init__(self, number_of_arms=3):
        self.number_of_arms = number_of_arms

        self.theta = [random.uniform(0, 359) for _ in range(number_of_arms)]
        self.x, self.y = 100, 100
        self.time = 0
        self.max_time = 2000

    def draw(self, win, x0, y0):
        for arm in range(self.number_of_arms):
            if self.theta[arm] > 360: self.theta[arm] = 0
            if self.theta[arm] < 0: self.theta[arm] = 360
            x, y = x0 + self.ARM_LENGTH * math.cos(math.radians(self.theta[arm])), y0 + self.ARM_LENGTH * math.sin(math.radians(self.theta[arm]))
            pygame.draw.line(win, self.COLOR, (x0, y0), (x, y), self.ARM_WIDTH)
            pygame.draw.circle(win, (0, 255, 0), (x, y), self.HINGE_RADIUS)
            x0, y0 = x, y
        self.x, self.y = x, y

    def rotate(self, arm, clockwise=True):
        if clockwise:
            self.theta[arm] += self.VEL
        else:
            self.theta[arm] -= self.VEL

    def reset(self, arm):
        self.theta[arm] = 0