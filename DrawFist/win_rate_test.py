from DrawFist.main import main

if __name__ == '__main__':
    robot_wins, draws, human_wins = 0, 0, 0
    for i in range(100):
        result = main()
        if result == 1:
            robot_wins += 1
        elif result == 0:
            draws += 1
        else:
            human_wins += 1
    print('')
    print('电脑final赢:', robot_wins, '玩家final赢:', human_wins, '平局final:', draws)
