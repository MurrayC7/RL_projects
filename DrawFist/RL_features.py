import random
import numpy as np

'''RL'''


class RL:
    def __init__(self):
        self.nwin = 0
        self.ntie = 0
        self.nloss = 0
        # iter = 0
        self.epsilon = 0.2
        self.actions = ['00', '01', '02', '03', '04', '05', '11', '12', '13', '14', '15', '16', '22', '23', '24', '25',
                        '26',
                        '27', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49', '55', '56', '57',
                        '58',
                        '59', '5!']
        self.RLscore = 0

        self.score = score_util(self.actions)

        self.Q = dict()
        self.lr = 0.9
        self.limits = [5, 15, 30]
        self.urmoves = ""
        self.mymoves = ""
        self.DNAmoves = ""

        self.nuclease = nuclease_util(self.actions, self.score)
        self.length = 0
        self.output = random.choice(self.actions)
        self.action = ""
        self.newstate = tuple()

    def play(self, inputs):
        # print("开始，出拳：")
        # train = True
        # STEP = 50

        # inputs = np.random.choice(actions)
        # print("人类：", inputs)
        # inputs = input("出拳 + 喊话：")

        if inputs != '':

            # History matching
            self.urmoves += inputs
            self.mymoves += self.output
            self.DNAmoves += self.nuclease[inputs + self.output]
            self.length += 1

            state = self.newstate
            self.newstate = []
            for z in range(2):
                limit = min([self.length, self.limits[z]])
                j = limit
                while j >= 1 and not self.DNAmoves[self.length - j:self.length] in self.DNAmoves[0:self.length - 1]:
                    j -= 1
                if j >= 1:
                    i = self.DNAmoves.rfind(self.DNAmoves[self.length - j:self.length], 0,
                                            self.length - 1)  # You seem to be playing based on our moves
                    self.newstate.append(self.urmoves[j + i])
                    self.newstate.append(self.mymoves[j + i])
                j = limit
                while j >= 1 and not self.urmoves[self.length - j:self.length] in self.urmoves[0:self.length - 1]:
                    j -= 1
                if j >= 1:
                    i = self.urmoves.rfind(self.urmoves[self.length - j:self.length], 0,
                                           self.length - 1)  # You seem to be playing based on your moves
                    self.newstate.append(self.urmoves[j + i])
                    self.newstate.append(self.mymoves[j + i])
                j = limit
                while j >= 1 and not self.mymoves[self.length - j:self.length] in self.mymoves[0:self.length - 1]:
                    j -= 1
                if j >= 1:
                    i = self.mymoves.rfind(self.mymoves[self.length - j:self.length], 0,
                                           self.length - 1)  # You seem to be playing based on my moves
                    self.newstate.append(self.urmoves[j + i])
                    self.newstate.append(self.mymoves[j + i])

            self.newstate = tuple(self.newstate)
            self.action = self.output
            #        print "program gives: %s" % output
            if self.score[(self.output, inputs)] == 1:
                self.nloss += 1
                self.RLscore += 1
            elif self.score[(self.output, inputs)] == 0:
                self.ntie += 1
                self.RLscore -= 0.5
            elif self.score[(self.output, inputs)] == -1:
                self.nwin += 1
                self.RLscore -= 1
            # if score[(output, inputs)] == -1 and random.random() < 0.5:
            #     self.RLscore = 0
            print("电脑RL出拳 + 喊话：", self.output)
            print('电脑RL赢:', self.nloss, '玩家RL赢:', self.nwin, '平局RL:', self.ntie)

            reward = self.score[(self.action, inputs)]
            maxvalue = max(self.Q.get((self.newstate, a), 0) for a in self.actions)
            self.Q[(state, self.action)] = self.Q.get((state, self.action), 0) + self.lr * (
                    reward + 0.5 * maxvalue - self.Q.get((state, self.action), 0))
            succ = [self.Q.get((self.newstate, a), 0) for a in self.actions]
            optimal_actions = [self.actions[x] for x in range(len(succ)) if succ[x] == max(succ)]
            self.output = random.choice(optimal_actions) if random.random() > self.epsilon else random.choice(
                self.actions)

        else:
            raise RuntimeWarning('Input is empty.')


def score_util(actions):
    result = {}
    gesture_1 = []
    voice_1 = []
    for i in range(len(actions)):
        gesture_1.append(int(actions[i][0]))
        if actions[i][1] != '!':
            voice_1.append(int(actions[i][1]))
        else:
            voice_1.append(10)

    gesture_2 = gesture_1
    voice_2 = voice_1

    for j in range(len(gesture_1)):
        for k in range(len(gesture_2)):
            if gesture_1[j] + gesture_2[k] == voice_1[j] and gesture_1[j] + gesture_2[k] != voice_2[k]:
                # result[j][k] = 1
                result[(actions[j], actions[k])] = 1
            elif gesture_1[j] + gesture_2[k] != voice_1[j] and gesture_1[j] + gesture_2[k] == voice_2[k]:
                # result[j][k] = -1
                result[(actions[j], actions[k])] = -1
            else:
                result[(actions[j], actions[k])] = 0
                # result[j][k] = 0
    return result


def nuclease_util(actions, score):
    nuclease = {}
    i = 0
    for a in actions:
        for b in actions:
            if score[(a, b)] == -1:
                nuclease[a + b] = str(i)
                i += 1
    for a in actions:
        for b in actions:
            if score[(a, b)] == 1:
                nuclease[a + b] = str(i)
                i += 1
    for a in actions:
        for b in actions:
            if score[(a, b)] == 0:
                nuclease[a + b] = str(i)
                i += 1
    return nuclease
