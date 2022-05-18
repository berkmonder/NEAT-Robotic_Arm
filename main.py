import pygame
import neat
import os
import time
import pickle
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Machine Spirit")
FPS = 60

# Colors
BLACK = (0, 0, 0)
BLUE = (75, 100, 255)
RED = (255, 100, 75)

class Arm:
    def __init__(self):
        self.x0 = 0 + WIDTH / 2
        self.y0 = 0 + HEIGHT / 2
        self.radius = 100
        self.theta = 0
        self.color = BLUE
        self.fixed = False

    def draw(self, win, prev_x, prev_y, theta):
        if self.fixed:
            x0 = self.x0
            y0 = self.y0
        else:
            x0 = prev_x
            y0 = prev_y

        theta = -theta

        x = x0 + self.radius * math.cos(theta)
        y = y0 + self.radius * math.sin(theta)

        pygame.draw.line(win, BLUE, (x0, y0), (x, y), 5)
        pygame.draw.circle(win, RED, (x, y), 5)
        return x, y

def main():
    run = True
    clock = pygame.time.Clock()

    arm1 = Arm()
    arm1.fixed = True

    arm2 = Arm()

    arm3 = Arm()

    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        theta1 = 0
        theta2 = 180
        theta3 = 360

        prev_x, prev_y = arm1.draw(WIN, 0, 0, theta1)
        prev_x, prev_y = arm2.draw(WIN, prev_x, prev_y, theta2)
        prev_x, prev_y = arm3.draw(WIN, prev_x, prev_y, theta3)

        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    run_neat(config)