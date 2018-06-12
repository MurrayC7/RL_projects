import random
import socket
import threading
import time

import numpy as np
from DrawFist.CFR import Game
from DrawFist.RL_features import RL

cfr = Game()
rl = RL()


def main():
    print("开始，出拳：")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 55555))

    s.listen(1)
    print('waiting for connection...')

    while 1:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


def tcplink(sock, addr):
    flag = True

    print('Accept new connection from %s:%s...' % addr)
    while True:
        data = sock.recv(1024)
        print(data)
        if 'nocheat' in data.decode('utf-8'):
            flag = True  # verify no cheat
            break
        elif 'quick' in data.decode('utf-8'):
            flag = False  # quick mode doesn't verify no cheat
            break
    time.sleep(1)
    if flag:
        nocheat_mode(sock)
    else:
        quick_mode(sock)
    sock.close()
    print('Connection from %s:%s closed' % addr)


def nocheat_mode(sock):
    final_nwin = 0
    final_ntie = 0
    final_nloss = 0
    score = rl.score
    inputs = ''

    while True:

        with open('HumanVoice.txt', 'r', encoding='utf-8') as frv:
            with open('HumanGesture.txt', 'r', encoding='utf-8') as frh:
                h_g = frh.readline().strip()
                h_v = frv.readline().strip()
        intg = int(h_g)
        if h_v == ':':
            intv = 10
        else:
            intv = int(h_v)
        if 6 < intv - intg < 0:
            h_v = h_g + 3
        if h_g and h_v and 6 > intv - intg > 0:
            inputs = h_g + h_v
        cfr.play(inputs)
        rl.play(inputs)

        if cfr.score > rl.RLscore:
            final_output = cfr.output
        elif cfr.score < rl.RLscore:
            final_output = rl.action
        else:
            final_output = random.choice([cfr.output, rl.action])
        print("predscore[game_rm.score, RLscore]: ", [cfr.score, rl.RLscore])
        # 0.96*(mScore[i]+(input==m[i])-(input==beat[beat[m[i]]])) + (random.random()-0.5)*dithering
        # random drop? naive drop? naive decay?

        # naive decay
        cfr.score *= 0.8
        rl.RLscore *= 0.8

        # if score[(final_output, inputs)] == 1:
        #     final_nloss += 1
        # elif score[(final_output, inputs)] == 0:
        #     final_ntie += 1
        # elif score[(final_output, inputs)] == -1:
        #     final_nwin += 1
        print("电脑final出拳 + 喊话：", final_output)
        # print('电脑final赢:', final_nloss, '玩家final赢:', final_nwin, '平局final:', final_ntie)
        with open('RobotVoice.txt', 'w', encoding='utf-8') as fwv:
            with open('RobotGesture.txt', 'w', encoding='utf-8') as fwh:
                fwv.write(str(final_output[1]))
                fwh.write(str(final_output[0]))
                print(final_output[0], final_output[1])
        with open('ActionTrigger.txt', 'w', encoding='utf-8') as ftrigger:
            ftrigger.write(str(1))

        with open('/home/esdc2018/桌面/Robot/RobotGesture.txt', 'rb') as rg:
            rgdata = rg.readline().strip()
        with open('/home/esdc2018/桌面/Robot/RobotVoice.txt', 'rb') as rv:
            rvdata = rv.readline().strip()

        sock.send(rgdata + rvdata)

        data = sock.recv(1024)
        print(data)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break

        if 'nocheat' not in data.decode('utf-8'):
            with open('/home/esdc2018/桌面/Robot/HumanVoice.txt', 'w') as hv:
                hv.write(str(data)[2])
            with open('/home/esdc2018/桌面/Robot/HumanGesture.txt', 'w') as hg:
                hg.write(str(data)[3])


def quick_mode(sock):
    final_nwin = 0
    final_ntie = 0
    final_nloss = 0
    score = rl.score
    inputs = ''

    while True:

        data = sock.recv(1024)
        print(data)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        # if 'nocheat' not in data.decode('utf-8') and 'quick' not in data.decode('utf-8'):
        h_v = str(data)[2]
        h_g = str(data)[3]

        intg = int(h_g)
        if h_v == ':':
            intv = 10
        else:
            intv = int(h_v)
        if 6 < intv - intg < 0:
            h_v = h_g + 3
        if h_g and h_v and 6 > intv - intg > 0:
            inputs = h_g + h_v

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
        cfr.score *= 0.8
        rl.RLscore *= 0.8

        with open('RobotVoice.txt', 'w', encoding='utf-8') as fwv:
            with open('RobotGesture.txt', 'w', encoding='utf-8') as fwh:
                fwv.write(str(final_output[1]))
                fwh.write(str(final_output[0]))
                print(final_output[0], final_output[1])
        with open('ActionTrigger.txt', 'w', encoding='utf-8') as ftrigger:
            ftrigger.write(str(1))

        with open('/home/esdc2018/桌面/Robot/RobotGesture.txt', 'rb') as rg:
            rgdata = rg.readline().strip()
        with open('/home/esdc2018/桌面/Robot/RobotVoice.txt', 'rb') as rv:
            rvdata = rv.readline().strip()

        sock.send(rgdata + rvdata)

        # if score[(final_output, inputs)] == 1:
        #     final_nloss += 1
        # elif score[(final_output, inputs)] == 0:
        #     final_ntie += 1
        # elif score[(final_output, inputs)] == -1:
        #     final_nwin += 1
        print("电脑final出拳 + 喊话：", final_output)
        # print('电脑final赢:', final_nloss, '玩家final赢:', final_nwin, '平局final:', final_ntie)


if __name__ == '__main__':
    main()
