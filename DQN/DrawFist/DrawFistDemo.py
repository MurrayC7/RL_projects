import random
import gym
import math
import numpy as np
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
from tensorflow.contrib.keras.python.keras.layers import Dense
from tensorflow.contrib.keras.python.keras.models import Sequential
from tensorflow.contrib.keras.python.keras.optimizers import Adam

N_STATES = 6  # the length of the 1 dimensional world
ACTIONS = range(36)  # available actions
print(ACTIONS)
EPSILON = 0.9  # greedy police
ALPHA = 0.1  # learning rate
GAMMA = 0.9  # discount factor
MAX_EPISODES = 1000  # maximum episodes
FRESH_TIME = 0.3  # fresh time for one move
STEP = 200
TEST = 10


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),  # q_table initial values
        columns=actions,  # actions's name
    )
    # print(table)    # show table
    return table


def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:  # act greedy
        action_name = state_actions.idxmax()  # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name


def choose_action_ngreedy(state, q_table):
    state_actions = q_table.iloc[state, :]
    return state_actions.idxmax()


class DrawFist:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def run(self):
        # main part of RL loop
        env = gym.make('DrawFist-v0')
        env.seed(1)
        total_reward = 0
        q_table = build_q_table(N_STATES, ACTIONS)
        for episode in range(MAX_EPISODES):
            observation = env.reset()
            for i in range(STEP):
                action = choose_action(observation, q_table)
                # action = int(action)
                # print('action:', action)
                observation_, reward, done, _ = env.step(action)
                q_predict = q_table.loc[observation, action]
                # print("total_reward", total_reward)
                if total_reward < 1000:
                    q_target = reward + GAMMA * q_table.iloc[observation_, :].max()  # next state is not terminal
                else:
                    q_target = reward  # next state is terminal
                    done = True  # terminate this episode
                total_reward += reward

                q_table.loc[observation, action] += ALPHA * (q_target - q_predict)  # update
                observation = observation_  # move to next state
                if done:
                    break
                # Test every 100 episodes
                if episode % 100 == 0:
                    total_reward_test = 0
                    for j in range(5):
                        state = random.randint(0, 5)
                        # for k in range(STEP):
                        # env.render()
                        action = choose_action_ngreedy(state, q_table)  # direct action for test
                        state, reward, done, info = env.step(action)
                        total_reward_test += reward
                        if done:
                            break
                            # print('info: g_h:{}, g_r:{}, voice:{}, guess:{}'.format(info['g_h'], info['g_r'],
                            #                                                         info['voice'],
                            #                                                         info['guess_count']))
                    ave_reward = total_reward_test
                    print('episode: ', episode, 'Evaluation Average Reward:', ave_reward)
                    # if ave_reward >= 200:
                    #     break

        return q_table


if __name__ == '__main__':
    agent = DrawFist('cc')
    print(agent.run())
