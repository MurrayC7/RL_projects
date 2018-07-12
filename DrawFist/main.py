import random
import numpy as np
from DrawFist.CFR import Game
from DrawFist.RL_features import RL
from DrawFist.win_rate_test import simple_strategy, complex_strategy

seq_n = 2
seq_length = 50


def main(STEP=3):
    final_nwin = 0
    final_ntie = 0
    final_nloss = 0

    print("开始，出拳：")

    cfr = Game()
    rl = RL()
    score = rl.score
    actions = rl.actions

    # test_seq = simple_strategy(n=seq_n)
    test_seq = complex_strategy(length=seq_length)

    for step in range(STEP):
        # print("")
        # print("")

        # from DrawFist.simulation import simulate
        # r = simulate('Gaussian')
        # inputs = np.random.choice(actions)

        # inputs = test_seq[step % (seq_n * 6)]
        inputs = test_seq[step % seq_length]
        print("人类：", inputs)
        # inputs = input("出拳 + 喊话：")

        if inputs != '':
            cfr.play(inputs)
            rl.play(inputs)
        else:
            continue
        if cfr.score > rl.RLscore:
            final_output = cfr.output
        elif cfr.score < rl.RLscore:
            final_output = rl.action
        else:
            final_output = random.choice([cfr.output, rl.action])
        # print("predscore[game_rm.score, RLscore]: ", [cfr.score, rl.RLscore])
        # 0.96*(mScore[i]+(input==m[i])-(input==beat[beat[m[i]]])) + (random.random()-0.5)*dithering
        # random drop? naive drop? naive decay?

        # naive decay
        cfr.score *= 0.5
        rl.RLscore *= 0.5

        if score[(final_output, inputs)] == 1:
            final_nloss += 1
        elif score[(final_output, inputs)] == 0:
            final_ntie += 1
        elif score[(final_output, inputs)] == -1:
            final_nwin += 1
        print("电脑final出拳 + 喊话：", final_output)
        print('电脑final赢:', final_nloss, '玩家final赢:', final_nwin, '平局final:', final_ntie)
    if final_nloss > final_nwin:
        return 1
    elif final_nloss < final_nwin:
        return -1
    else:
        return 0
    # print(Q)
    # print(mymoves)
    # print(urmoves)
    # print(DNAmoves)
    # print(newstate)
    # print(state)


if __name__ == '__main__':
    robot_wins, draws, human_wins = 0, 0, 0
    for i in range(2):
        result = main(2 * seq_length)
        if result == 1:
            robot_wins += 1
        elif result == 0:
            draws += 1
        else:
            human_wins += 1
    print('电脑final测试赢:', robot_wins, '玩家final测试赢:', human_wins, '平局final测试:', draws)
    # main()
