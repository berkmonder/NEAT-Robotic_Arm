import pygame
import math
import random
from .arm import Arm

class Food:
    COLOR = (255, 0, 0) # RED
    RADIUS = 5

    def __init__(self):
        self.distance, self.angle = self.reset()
        self.x, self.y = 0, 0

    def reset(self):
        self.distance, self.angle = random.uniform(0, 3*Arm.ARM_LENGTH), random.uniform(0, 360)
        return self.distance, self.angle

    def draw(self, window, window_width, window_height):
        self.x, self.y = window_width + self.distance * math.cos(math.radians(self.angle)),\
                        window_height + self.distance * math.sin(math.radians(self.angle))
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.RADIUS)