import pygame
import math
import random
from .arm import Arm

class Food:
    COLOR = (255, 0, 0) # RED
    RADIUS = 5

    def __init__(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.distance, self.angle = self.reset()
        self.x, self.y = 0, 0

    def reset(self):
        self.distance, self.angle = random.uniform(0, Arm.ARM_LENGTH * 2), random.uniform(0, 359)
        return self.distance, self.angle

    def draw(self, window):
        self.x, self.y = self.x_offset + self.distance * math.cos(math.radians(self.angle)),\
                        self.y_offset + self.distance * math.sin(math.radians(self.angle))
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.RADIUS)