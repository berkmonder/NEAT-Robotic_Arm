import os
import pickle
import gym
import neat
import numpy as np

with open('winner', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

env = gym.make("Acrobot-v1")
observation = env.reset()

done = False
while not done:
    action = np.argmax(net.activate(observation))

    observation, reward, done, info = env.step(env.action_space.sample())
    env.render()
