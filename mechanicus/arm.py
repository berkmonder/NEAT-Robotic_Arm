import pygame
import numpy as np

import math
import random

class Arm:
    COLOR = (0, 0, 255) # BLUE
    VEL = 2
    ARM_LENGTH = 100
    ARM_WIDTH = 3
    HEAD_RADIUS = 5

    def __init__(self, number_of_arms, x_offset, y_offset):
        self.number_of_arms = number_of_arms
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.MAX_RADIUS = number_of_arms * self.ARM_LENGTH
        self.angle = np.random.uniform(0, 359, self.number_of_arms)
        self.x, self.y = np.ones(number_of_arms) * self.ARM_LENGTH, np.zeros(number_of_arms)

        self.time = 0
        self.max_time = 2000
        self.score = 0

    def draw(self, win):
        x0, y0 = self.x_offset, self.y_offset
        for index in range(self.number_of_arms):
            self.x[index], self.y[index] = x0 + self.ARM_LENGTH * math.cos(math.radians(self.angle[index])),\
                                           y0 + self.ARM_LENGTH * math.sin(math.radians(self.angle[index]))

            pygame.draw.line(win, self.COLOR, (x0, y0), (self.x[index], self.y[index]), self.ARM_WIDTH)
            pygame.draw.circle(win, (0, 255, 0), (self.x[index], self.y[index]), self.HEAD_RADIUS)
            x0, y0 = self.x[index], self.y[index]

    def rotate(self, arm_number, clockwise=True):
        for arm in range(arm_number+1):
            if clockwise:
                self.angle[arm] += self.VEL
            else:
                self.angle[arm] -= self.VEL

    def random_angle(self):
        self.angle = np.random.uniform(0, 359, self.number_of_arms)