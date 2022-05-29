from turtle import width
import pygame
import os
import math
import sys
import random
import neat

screen_width = 1500
screen_height = 800
generation = 0

class Arm:
    def __init__(self):
        self.surface = pygame.image.load("arm.png")
        self.surface = pygame.transform.scale(self.surface, (300, 100))
        self.rotate_surface = self.surface
        self.pos = [screen_width//2, screen_height//2]
        self.angle = 0
        self.center = [self.pos[0] + 83, self.pos[1] + 107]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.goal = False
        self.food_eaten = 0
        self.time_spent = 0

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        # screen.draw_radar(screen)

    def draw_radar(self, screen):
        for r in self.radars:
            pos, dist = r
            pygame.draw.line(screen, (0, 255, 0), self.head, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    def check_collision(self, food):
        self.is_alive = True
        for p in self.four_points:
            if food.get_at((int(p[0]), int(p[1]))) == (255, 0, 0, 255):
                self.food_eaten += 1
                # TODO: Reset food position
                print(self.food_eaten)
                break

    def check_radar(self, degree, map):
        pass

    def update(self, food):
        self.rotate_surface = self.rot_center(self.surface, self.angle)

    def get_data(self):
        radars = self.radars
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1] / 30)

        return ret

    def get_alive(self):
        return self.is_alive

    def get_reward(self):
        return self.food_eaten

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

def run_arm(genomes, config):

    # Init NEAT
    nets = []
    arms = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        # Init my arms
        arms.append(Arm())

    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)
    food = pygame.image.load('food.png')
    food = pygame.transform.scale(food, (50, 50))


    # Main loop
    global generation
    generation += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Input my data and get result from network
        for index, arm in enumerate(arms):
            output = nets[index].activate(arm.get_data())
            i = output.index(max(output))
            if i == 0:
                arm.angle += 10
            else:
                arm.angle -= 10

        # Update arm and fitness
        remain_arms = 0
        for i, arm in enumerate(arms):
            if arm.get_alive():
                remain_arms += 1
                arm.update(food)
                genomes[i][1].fitness += arm.get_reward()

        # check
        if remain_arms == 0:
            break

        # Drawing
        screen.fill((255, 255, 255))
        screen.blit(food, (screen_width/2+100, screen_height/2-20)) # TODO: what the hell
        for arm in arms:
            if arm.get_alive():
                arm.draw(screen)

        text = generation_font.render("Generation : " + str(generation), True, (255, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width/2, 100)
        screen.blit(text, text_rect)

        text = font.render("remain arms : " + str(remain_arms), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width/2, 200)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(0)

if __name__ == "__main__":
    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run_arm, 1000)
