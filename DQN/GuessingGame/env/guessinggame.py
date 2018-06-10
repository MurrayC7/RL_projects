import numpy as np
import gym
from gym import spaces
from gym.utils import seeding


class GuessingGame(gym.Env):
    # def __init__(self):
    #     self.action_space = spaces.Discrete(6)
    #     self.observation_space = spaces.Discrete(2)
    #     self._seed()
    #     self._state = self._reset()
    #
    # def _step(self, action):
    #     assert self.action_space.contains(action)
    #     return self._state, 1000 if action == self._state.sum() else -abs(
    #         action - self._state.sum()), action == self._state.sum(), {}
    #
    # def _reset(self):
    #     a = self.np_random.choice([i for i in range(int(self.action_space.n / 2))])
    #     b = self.np_random.choice([i for i in range(int(self.action_space.n / 2))])
    #     self._state = np.array([a, b], dtype=np.float32)
    #     return self._state
    #
    # def get_state(self):
    #     return self._state
    #
    # def _configure(self):
    #     pass
    #
    # def _seed(self, seed=None):
    #     self.np_random, seed = seeding.np_random(seed)
    #     return [seed]
    def __init__(self):
        self.range = 1000  # Randomly selected number is within +/- this value
        self.bounds = 1000

        self.action_space = spaces.Box(low=np.array([0]), high=np.array([self.bounds]))
        self.observation_space = spaces.Discrete(4)

        self.number = 0
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

        if action < self.number:
            self.observation = 1

        elif action == self.number:
            self.observation = 2

        elif action > self.number:
            self.observation = 3

        reward = 0
        done = False

        if (self.number - self.range * 0.01) < action < (self.number + self.range * 0.01):
            reward = 1
            done = True

        self.guess_count += 1
        if self.guess_count >= self.guess_max:
            done = True

        return self.observation, reward, done, {"number": self.number, "guesses": self.guess_count}

    def reset(self):
        self.number = self.np_random.uniform(0, self.range)
        self.guess_count = 0
        self.observation = 0
        return self.observation
