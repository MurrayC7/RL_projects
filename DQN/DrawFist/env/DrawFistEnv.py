import gym
from gym import spaces
from gym.utils import seeding
import numpy as np


class DrawFist(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(36)
        self.observation_space = spaces.Discrete(4)

        self.g_h = 0
        self.g_r = 0
        self.v_r = 0
        self.guess_count = 0
        self.guess_max = 200
        self.observation = 0

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)

        if action < self.g_r + self.g_h:
            self.observation = 1

        elif action == self.g_r + self.g_h:
            self.observation = 2

        elif action > self.g_r + self.g_h:
            self.observation = 3

        reward = 0
        done = False

        if action == self.g_r + self.g_h:
            reward = 1
            done = True

        self.guess_count += 1
        if self.guess_count >= self.guess_max:
            done = True

        return self.observation, reward, done, {"g_h": self.g_h, "g_r": self.g_r, "guesses": self.guess_count}

    def reset(self):
        self.g_h = self.np_random.uniform(0, 5)
        self.g_r = self.np_random.uniform(0, 5)
        self.guess_count = 0
        self.observation = 0
        return self.observation
