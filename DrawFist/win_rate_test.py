# from DrawFist.main import main
import math

actions = ['00', '01', '02', '03', '04', '05', '11', '12', '13', '14', '15', '16', '22', '23', '24', '25', '26',
           '27', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49', '55', '56', '57', '58',
           '59', '5!']


def simple_strategy(n):
    test_seq = [0] * (n * 6)
    for i in range(n):
        for j in range(6):
            test_seq[i * 6 + j] = str(j) + str(j + 1)
    print(test_seq)
    return test_seq


def complex_strategy(length):
    test_seq = [0] * length
    for i in range(length):
        fx = round(i ** 2 + math.log((i ** 3 - i) / (i ** 2 + 1) ** 2 + 2) * math.sin(math.sqrt(i)) ** 2 + i + 1)
        idx = fx % 36
        test_seq[i] = actions[idx]
    print(test_seq)
    return test_seq

#
# if __name__ == '__main__':
#     robot_wins, draws, human_wins = 0, 0, 0
#     for i in range(100):
#         result = main()
#         if result == 1:
#             robot_wins += 1
#         elif result == 0:
#             draws += 1
#         else:
#             human_wins += 1
#     print('')
#     print('电脑final赢:', robot_wins, '玩家final赢:', human_wins, '平局final:', draws)
