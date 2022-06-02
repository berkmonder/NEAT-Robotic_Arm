import pygame, math
from mechanicus import Game
import neat
import os
import pickle

from mechanicus.arm import Arm
from mechanicus.food import Food

GEN = 0
FPS = 1000
clock = pygame.time.Clock()

class RoboticArm:

    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.arm = self.game.arm
        self.food = self.game.food

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((math.sqrt((self.arm.x[-1] - self.food.x)**2 + (self.arm.y[-1] - self.food.y)**2), (self.arm.angle[-1] + self.arm.angle[-2])/2 - self.food.angle))
            decision = output.index(max(output))
            
            if decision == 0:
                self.game.rotate_arm(self.arm, 0, True)
            elif decision == 1:
                self.game.rotate_arm(self.arm, 0, False)
            elif decision == 2:
                self.game.rotate_arm(self.arm, 1, True)
            elif decision == 3:
                self.game.rotate_arm(self.arm, 1, False)
            else:
                pass

            game_info = self.game.loop(net, [self.arm], [self.food], [genome])
            self.game.draw([self.arm], [self.food], GEN)
            pygame.display.update()
            
        pygame.quit()

    def train_ai(self, nets, arms, foods, genomes, config):
        time = 0
        run = True
        global GEN
        GEN += 1
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


            for i, (arm, food) in enumerate(zip(arms, foods)):
                arm.time += clock.get_time()

                output = nets[i].activate((math.sqrt((arm.x[-1] - food.x)**2 + (arm.y[-1] - food.y)**2), (arm.angle[-1] + arm.angle[-2])/2 - food.angle))
                decision = output.index(max(output))

                if decision == 0:
                    self.game.rotate_arm(arm, 0, True)
                elif decision == 1:
                    self.game.rotate_arm(arm, 0, False)
                elif decision == 2:
                    self.game.rotate_arm(arm, 1, True)
                elif decision == 3:
                    self.game.rotate_arm(arm, 1, False)
                else:
                    pass

                # if self.game.score >= 500:
                if genomes[i].fitness >= 500:
                    run = False
                    break

            

            if len(arms) < 1:
                # self.caculate_fitness(genome, game_info)
                run = False
                break

            game_info = self.game.loop(nets, arms, foods, genomes)
            self.game.draw(arms, foods, GEN-1)

            pygame.display.update()

    def caculate_fitness(self, genome, game_info):
        genome.fitness += game_info.score

def eval_genomes(genomes, config):
    width, height = 800, 800
    window = pygame.display.set_mode((width, height))

    nets = []
    arms = []
    foods = []
    ge = []
    game = RoboticArm(window, width, height)
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        arms.append(Arm(2, width//2, height//2))
        foods.append(Food(width//2, height//2))
        genome.fitness = 0
        ge.append(genome)

    game.train_ai(nets, arms, foods, ge, config)

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint(f'neat-checkpoint-{GEN}')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    width, height = 800, 800
    window = pygame.display.set_mode((width, height))
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = RoboticArm(window, width, height)
    game.test_ai(winner, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
    # test_ai(config)