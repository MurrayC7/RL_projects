from __future__ import division
import numpy as np
import pandas as pd
import socket, threading, time, os, termios, sys

'''
    Use regret-matching algorithm to play DrawFist.
'''

regret_decay = 20000
regret_weight = 1

class DF:
    actions = ['00', '01', '02', '03', '04', '05', '11', '12', '13', '14', '15', '16', '22', '23', '24', '25', '26',
               '27', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49', '55', '56', '57', '58',
               '59', '5:']
    n_actions = 36
    utilities = pd.DataFrame

    @staticmethod
    def util():
        gesture_1 = []
        voice_1 = []
        for i in range(len(DF.actions)):
            gesture_1.append(int(DF.actions[i][0]))
            if DF.actions[i][1] != ':':
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
    def __init__(self, max_game=7):
        self.p1 = Player('robot')
        self.p2 = Player('human')
        self.max_game = max_game

        self.robot_wins = 0
        self.draws = 0

    def winner(self, a1, a2):
        result = DF.utilities.loc[a1, a2]
        if result == 1:
            return self.p1
        elif result == -1:
            return self.p2
        else:
            return 'Draw'

    def play(self, avg_regret_matching=False, train=False):
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
                    num_wins[winner] += 1
                    np.savetxt('regret_sum.txt', self.p1.regret_sum)
            # add file input
            else:
                #self.p1.regret_sum = np.loadtxt('regret_sum.txt')
                #self.p1.regret_sum = self.p1.regret_sum / regret_decay
                print("开始，出拳：")
                #termikeyset()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('0.0.0.0', 55555))

                s.listen(1)
                print('waiting for connection...')
                
                while 1:
                            sock, addr = s.accept()
                            t = threading.Thread(target=tcplink, args=(sock, addr))
                            t.start()                             

        def tcplink(sock, addr):
          print('Accept new connection from %s:%s...'% addr)
          while True:
                data = sock.recv(1024)
                print(data)
                if 'nocheat' in data.decode('utf-8'):
                   break
          while True:
           
                self.p1.update_strategy()
                a1 = self.p1.action()
                with open('RobotVoice.txt', 'w', encoding='utf-8') as fwv:
                     with open('RobotGesture.txt', 'w', encoding='utf-8') as fwh:
                          fwv.write(str(a1[1]))
                          fwh.write(str(a1[0]))
                          print(a1[0], a1[1])
                with open('ActionTrigger.txt', 'w', encoding='utf-8') as ftrigger:
                     ftrigger.write(str(1))
                with open('HumanVoice.txt', 'r', encoding='utf-8') as frv:
                     with open('HumanGesture.txt', 'r', encoding='utf-8') as frh:
                          h_g = frh.readline().strip()
                          h_v = frv.readline().strip()
                intg = int(h_g)
                if h_v==':':
                   intv = 10
                else: 
                   intv = int(h_v)
                if intv-intg>6 and intv-intg<0:
                     h_v = h_g + 3 
                if h_g and h_v and intv-intg<6 and intv-intg>0:
                   a2 = h_g + h_v
                   self.p1.regret(a1, a2, train=True)
                   winner = self.winner(a1, a2)
                   num_wins[winner] += 1

                with open('/home/esdc2018/桌面/Robot/RobotGesture.txt','rb') as rg:
                     rgdata = rg.readline().strip()
                with open('/home/esdc2018/桌面/Robot/RobotVoice.txt','rb') as rv:
                     rvdata = rv.readline().strip()
                
                sock.send(rgdata+rvdata)

                data = sock.recv(1024)
                print(data)
                time.sleep(1)
                if not data or data.decode('utf-8') == 'exit':
                     break

                if 'nocheat' not in data.decode('utf-8'):
                   with open('/home/esdc2018/桌面/Robot/HumanVoice.txt','w') as hv:
                     hv.write(str(data)[2])
                   with open('/home/esdc2018/桌面/Robot/HumanGesture.txt','w') as hg:
                     hg.write(str(data)[3])
          sock.close()
          print('Connection from %s:%s closed'% addr)

        def play_avg_regret_matching():
            for i in range(0, self.max_game):
                a1 = self.p1.action(use_avg=True)
                a2 = self.p2.action(use_avg=True)
                # a2 = np.random.choice(DF.actions)
                winner = self.winner(a1, a2)
                num_wins[winner] += 1

        num_wins = {
            self.p1: 0,
            self.p2: 0,
            'Draw': 0
        }

        play_regret_matching() if not avg_regret_matching else play_avg_regret_matching()
        print(num_wins)

        if num_wins[self.p1] > num_wins[self.p2]:
            self.robot_wins += 1
        elif num_wins[self.p1] == num_wins[self.p2]:
            self.draws += 1

    def conclude(self):
        """
        let two players conclude the average strategy from the previous strategy stats
        """
        self.p1.learn_avg_strategy()
        self.p2.learn_avg_strategy()



if __name__ == '__main__':

    game = Game(max_game=10000)
    episode = 100
    # print('==== Use simple regret-matching strategy === ')
    #for i in range(episode):
    game.play(train=False)
    #print("robot_wins:{}, draws:{}, human_wins:{}".format(game.robot_wins, game.draws,
    #                                                      episode - game.robot_wins - game.draws))

    # print('==== Use averaged regret-matching strategy === ')
    # game.conclude()
    # game.play(avg_regret_matching=True)
