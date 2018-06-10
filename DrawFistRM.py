from __future__ import division

import random

import numpy as np
import pandas as pd

'''
    Use regret-matching algorithm to play DrawFist.
'''

regret_decay = 200
regret_weight = 1


class DF:
    actions = ['00', '01', '02', '03', '04', '05', '11', '12', '13', '14', '15', '16', '22', '23', '24', '25', '26',
               '27', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49', '55', '56', '57', '58',
               '59', '5!']
    n_actions = 36
    utilities = pd.DataFrame

    @staticmethod
    def util():
        gesture_1 = []
        voice_1 = []
        for i in range(len(DF.actions)):
            gesture_1.append(int(DF.actions[i][0]))
            if DF.actions[i][1] != '!':
                voice_1.append(int(DF.actions[i][1]))
            else:
                voice_1.append(10)

        gesture_2 = gesture_1
        voice_2 = voice_1
        # print(gesture_1)
        # print(voice_1)

        result = np.zeros((DF.n_actions, DF.n_actions), dtype=int)
        for j in range(len(gesture_1)):
            for k in range(len(gesture_2)):
                if gesture_1[j] + gesture_2[k] == voice_1[j] and gesture_1[j] + gesture_2[k] != voice_2[k]:
                    result[j][k] = 1
                elif gesture_1[j] + gesture_2[k] != voice_1[j] and gesture_1[j] + gesture_2[k] == voice_2[k]:
                    result[j][k] = -1
                else:
                    result[j][k] = 0
        DF.utilities = pd.DataFrame(result, columns=DF.actions, index=DF.actions)


DF.util()


# print(DF.utilities)

class Player:
    def __init__(self, name):
        self.strategy, self.avg_strategy, \
        self.strategy_sum, self.regret_sum = np.zeros((4, DF.n_actions))
        self.name = name

    def __repr__(self):
        return self.name

    def update_strategy(self):
        """
        set the preference (strategy) of choosing an action to be proportional to positive regrets
        e.g, a strategy that prefers PAPER can be [0.2, 0.6, 0.2]
        """
        self.strategy = np.copy(self.regret_sum)
        self.strategy[self.strategy < 0] = 0  # reset negative regrets to zero

        summation = sum(self.strategy)
        if summation > 0:
            # normalise
            self.strategy /= summation
        else:
            # uniform distribution to reduce exploitability
            self.strategy = np.repeat(1 / DF.n_actions, DF.n_actions)

        self.strategy_sum += self.strategy

    def regret(self, my_action, opp_action, train=True):
        """
        we here define the regret of not having chosen an action
        as the difference between the utility of that action
        and the utility of the action we actually chose,
        with respect to the fixed choices of the other player.
        compute the regret and add it to regret sum.
        """
        if train:
            result = DF.utilities.loc[my_action, opp_action]
            facts = DF.utilities.loc[:, opp_action].values
            regret = facts - result
            self.regret_sum += regret
        else:
            result = DF.utilities.loc[my_action, opp_action]
            facts = DF.utilities.loc[:, opp_action].values
            regret = facts - result
            self.regret_sum += regret_weight * regret

    def action(self, use_avg=False):
        """
        select an action according to strategy probabilities
        """
        strategy = self.avg_strategy if use_avg else self.strategy
        return np.random.choice(DF.actions, p=strategy)

    def learn_avg_strategy(self):
        # averaged strategy converges to Nash Equilibrium
        summation = sum(self.strategy_sum)
        if summation > 0:
            self.avg_strategy = self.strategy_sum / summation
        else:
            self.avg_strategy = np.repeat(1 / DF.n_actions, DF.n_actions)


class Game:
    def __init__(self, max_game=7, init_score=0):
        self.p1 = Player('robot')
        self.p2 = Player('human')
        self.max_game = max_game
        self.score = init_score

        self.robot_wins = 0
        self.draws = 0

        self.output = ''
        self.num_wins = {
            self.p1: 0,
            self.p2: 0,
            'Draw': 0
        }

        self.p1.regret_sum = np.loadtxt('regret_sum.txt')
        self.p1.regret_sum = self.p1.regret_sum / regret_decay

    def winner(self, a1, a2):
        result = DF.utilities.loc[a1, a2]
        if result == 1:
            return self.p1
        elif result == -1:
            return self.p2
        else:
            return 'Draw'

    def play(self, h_input, avg_regret_matching=False, train=False):
        def play_regret_matching():
            if train:
                x = 0.5 * np.random.randn(36) + 0.5
                has_neg = False
                for neg in x < 0:
                    if neg:
                        has_neg = True
                if has_neg:
                    x = x - 1.5 * np.min(x)
                y = np.sum(x)
                r = x / y
                for i in range(0, self.max_game):
                    self.p1.update_strategy()
                    a1 = self.p1.action()
                    a2 = np.random.choice(DF.actions, p=r)
                    self.p1.regret(a1, a2)
                    winner = self.winner(a1, a2)
                    self.num_wins[winner] += 1
                    # np.savetxt('regret_sum.txt', self.p1.regret_sum)
            # add file input
            else:

                self.p1.update_strategy()
                a1 = self.p1.action()
                a2 = h_input
                self.p1.regret(a1, a2, train=True)
                self.output = a1
                winner = self.winner(a1, a2)
                if winner == self.p1:
                    self.robot_wins += 1
                    self.score += 1
                elif winner == 'Draw':
                    self.draws += 1
                    self.score -= 0.5
                else:
                    self.score -= 1
                # if winner == self.p2 and random.random() < 0.5:
                #     self.score = 0

                self.num_wins[winner] += 1
                # print("电脑RM出拳 + 喊话：", self.output)
                # np.savetxt('regret_sum_test.txt', self.p1.regret_sum)
                # print("开始，出拳：")
                # while 1:
                #     with open('1.txt', 'r') as fin:
                #         flag = fin.readline().strip()
                #         if flag == '1':
                #             self.p1.update_strategy()
                #             a1 = self.p1.action()
                #             with open('4.txt', 'w', encoding='utf-8') as fwv:
                #                 with open('5.txt', 'w', encoding='utf-8') as fwh:
                #                     fwv.write(str(a1[1]))
                #                     fwh.write(str(a1[0]))
                #                     print(a1[0], a1[1])
                #             with open('6.txt', 'r', encoding='utf-8') as frv:
                #                 with open('7.txt', 'r', encoding='utf-8') as frh:
                #                     h_g = frh.readline().strip()
                #                     print('h_g:', h_g)
                #                     h_v = frv.readline().strip()
                #             a2 = h_g + h_v
                #             self.p1.regret(a1, a2, train=True)
                #             winner = self.winner(a1, a2)
                #             num_wins[winner] += 1
                #             with open('1.txt', 'w+') as finw:
                #                 finw.write(str(0))

        def play_avg_regret_matching():
            for i in range(0, self.max_game):
                a1 = self.p1.action(use_avg=True)
                a2 = self.p2.action(use_avg=True)
                # a2 = np.random.choice(DF.actions)
                winner = self.winner(a1, a2)
                self.num_wins[winner] += 1

        play_regret_matching() if not avg_regret_matching else play_avg_regret_matching()
        # print(self.num_wins)


    def conclude(self):
        """
        let two players conclude the average strategy from the previous strategy stats
        """
        self.p1.learn_avg_strategy()
        self.p2.learn_avg_strategy()


# if __name__ == '__main__':
#     game = Game(max_game=10000)
#     episode = 100
#     for i in range(episode):
#         game.play(input("go:"))

#     print("robot_wins:{}, draws:{}, human_wins:{}".format(game.robot_wins, game.draws,
#                                                           episode - game.robot_wins - game.draws))
#
#     # print('==== Use averaged regret-matching strategy === ')
#     # game.conclude()
#     # game.play(avg_regret_matching=True)
