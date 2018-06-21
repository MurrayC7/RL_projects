import random
import numpy as np
from DrawFistRM import Game, Player, DF

x = 0.5 * np.random.randn(36) + 0.5
has_neg = False
for neg in x < 0:
    if neg:
        has_neg = True
if has_neg:
    x = x - 1.5 * np.min(x)
y = np.sum(x)
r = x / y


def main(STEP):
    DF.util()

    """RL"""
    final_nwin = 0
    final_ntie = 0
    final_nloss = 0

    nwin = 0
    ntie = 0
    nloss = 0
    iter = 0
    epsilon = 0.2
    # inputs = ""
    # while True:
    actions = ['00', '01', '02', '03', '04', '05', '11', '12', '13', '14', '15', '16', '22', '23', '24', '25', '26',
               '27', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49', '55', '56', '57', '58',
               '59', '5!']
    n_actions = 36
    RLscore = 0

    def util():
        result = {}
        gesture_1 = []
        voice_1 = []
        for i in range(n_actions):
            gesture_1.append(int(actions[i][0]))
            if actions[i][1] != '!':
                voice_1.append(int(actions[i][1]))
            else:
                voice_1.append(10)

        gesture_2 = gesture_1
        voice_2 = voice_1
        # print(gesture_1)
        # print(voice_1)

        # result = np.zeros((n_actions, n_actions), dtype=int)
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

    score = util()

    # print(score)
    # score = {
    #     ('R', 'R'): 0, ('R', 'P'): -1, ('R', 'S'): 1,
    #     ('P', 'R'): 1, ('P', 'P'): 0, ('P', 'S'): -1,
    #     ('S', 'R'): -1, ('S', 'P'): 1, ('S', 'S'): 0
    # }
    Q = dict()
    lr = 0.9
    limits = [5, 15, 30]
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}
    urmoves = ""
    mymoves = ""
    DNAmoves = ""

    def nuclease_util():
        nuclease = {}
        i = 0
        for a in actions:
            for b in actions:
                if score[(a, b)] == -1:
                    nuclease[a + b] = str(i)
                    i += 1
        for a in actions:
            for b in actions:
                if score[(a, b)] > 0:
                    nuclease[a + b] = str(i)
                    i += 1
        for a in actions:
            for b in actions:
                if score[(a, b)] == 0:
                    nuclease[a + b] = str(i)
                    i += 1
        return nuclease

    nuclease = nuclease_util()
    # print(nuclease)
    # nuclease = {'RP': 'a', 'PS': 'b', 'SR': 'c', 'PR': 'd', 'SP': 'e', 'RS': 'f', 'RR': 'g', 'PP': 'h', 'SS': 'i'}
    length = 0
    output = random.choice(actions)
    newstate = tuple()

    # print("开始，出拳：")
    train = True

    game_rm = Game(max_game=STEP)
    game_human = Game(max_game=STEP)

    for step in range(STEP):
        # print("")
        print("")

        # inputs = np.random.choice(actions)
        game_human.play(output)
        inputs = game_human.output
        print("人类：", inputs)

        # inputs = input("出拳 + 喊话：")

        if inputs != '':
            """RM"""

            game_rm.play(inputs)

            # History matching
            urmoves += inputs
            mymoves += output
            DNAmoves += nuclease[inputs + output]
            length += 1

            state = newstate
            newstate = []
            for z in range(2):
                limit = min([length, limits[z]])
                j = limit
                while j >= 1 and not DNAmoves[length - j:length] in DNAmoves[0:length - 1]:
                    j -= 1
                if j >= 1:
                    i = DNAmoves.rfind(DNAmoves[length - j:length], 0,
                                       length - 1)  # You seem to be playing based on our moves
                    newstate.append(urmoves[j + i])
                    newstate.append(mymoves[j + i])
                j = limit
                while j >= 1 and not urmoves[length - j:length] in urmoves[0:length - 1]:
                    j -= 1
                if j >= 1:
                    i = urmoves.rfind(urmoves[length - j:length], 0,
                                      length - 1)  # You seem to be playing based on your moves
                    newstate.append(urmoves[j + i])
                    newstate.append(mymoves[j + i])
                j = limit
                while j >= 1 and not mymoves[length - j:length] in mymoves[0:length - 1]:
                    j -= 1
                if j >= 1:
                    i = mymoves.rfind(mymoves[length - j:length], 0,
                                      length - 1)  # You seem to be playing based on my moves
                    newstate.append(urmoves[j + i])
                    newstate.append(mymoves[j + i])

            newstate = tuple(newstate)
            action = output
            #        print "program gives: %s" % output
            if score[(output, inputs)] > 0:
                nloss += 1
                RLscore += 5
            elif score[(output, inputs)] == 0:
                ntie += 1
                RLscore -= 0.5
            elif score[(output, inputs)] == -1:
                nwin += 1
                RLscore -= 5
            # if score[(output, inputs)] == -1 and random.random() < 0.5:
            #     RLscore = 0
            # print("电脑RL出拳 + 喊话：", output)
            # print('电脑RL赢:', nloss, '玩家RL赢:', nwin, '平局RL:', ntie)

            reward = score[(action, inputs)]
            succ = [Q.get((newstate, a), 0) for a in actions]
            optimal_actions_ = [actions[x] for x in range(len(succ)) if succ[x] == max(succ)]
            action_ = random.choice(optimal_actions_) if random.random() > epsilon else random.choice(actions)
            maxvalue = Q.get((newstate, action_), 0)
            Q[(state, action)] = Q.get((state, action), 0) + lr * (reward + 0.8 * maxvalue - Q.get((state, action), 0))
            output = action_

            # reward = score[(action, inputs)]
            # maxvalue = max(Q.get((newstate, a), 0) for a in actions)
            # Q[(state, action)] = Q.get((state, action), 0) + lr * (reward + 0.8 * maxvalue - Q.get((state, action), 0))
            # succ = [Q.get((newstate, a), 0) for a in actions]
            # optimal_actions = [actions[x] for x in range(len(succ)) if succ[x] == max(succ)]
            # output = random.choice(optimal_actions) if random.random() > epsilon else random.choice(actions)
        else:
            continue
        if game_rm.score > RLscore:
            final_output = game_rm.output
        elif game_rm.score < RLscore:
            final_output = action
        else:
            final_output = random.choice([game_rm.output, action])
        # final_output = action
        # print("predscore[game_rm.score, RLscore]: ", [game_rm.score, RLscore])
        # 0.96*(mScore[i]+(input==m[i])-(input==beat[beat[m[i]]])) + (random.random()-0.5)*dithering
        # random drop? naive drop? naive decay?

        # naive decay
        game_rm.score *= 0.5
        RLscore *= 0.5

        if score[(final_output, inputs)] == 1:
            final_nloss += 1
        elif score[(final_output, inputs)] == 0:
            final_ntie += 1
        elif score[(final_output, inputs)] == -1:
            final_nwin += 1
        print("电脑final出拳 + 喊话：", final_output)
        print('电脑赢:', final_nloss, '玩家赢:', final_nwin, '平局:', final_ntie)

    return final_nloss, final_nwin, final_ntie
    # if final_nloss > final_nwin:
    #     return 1
    # elif final_nloss < final_nwin:
    #     return -1
    # else:
    #     return 0


if __name__ == '__main__':
    # robot_wins, draws, human_wins = 0, 0, 0
    # for i in range(10):
    #     result = main(STEP=1)
    #     if result == 1:
    #         robot_wins += 1
    #     elif result == 0:
    #         draws += 1
    #     else:
    #         human_wins += 1
    # print('电脑final赢:', robot_wins, '玩家final赢:', human_wins, '平局final:', draws)
    final_nloss, final_nwin, final_ntie = main(10000)
    print('电脑final赢:', final_nloss, '玩家final赢:', final_nwin, '平局final:', final_ntie)
