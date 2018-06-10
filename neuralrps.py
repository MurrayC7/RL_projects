# See http://overview.cc/RockPaperScissors for more information about rock, paper, scissors
# Trying out a new approach. Use a neural network. The weights are adjusted using an
# evolutionary technique.

if input == "":
    from collections import defaultdict
    import random
    import operator
    from itertools import izip, chain, islice
    split = {'R': [1, 0, 0], 'P': [1, 0, 1], 'S': [0, 0, 1], '':[0, 0, 01],
            'PS':[0, 0.5, 0.5], 'PR': [0.5, 0.5, 0] , 'RS':[0.5, 0, 0.5],
            'SR':[0, 0.5, 0.5], 'RP': [0.5, 0.5, 0] , 'SR':[0.5, 0, 0.5],
            'PRS': [0.33, 0.33, 0.33], 'PSR': [0.33, 0.33, 0.33], 'RPS': [0.33, 0.33, 0.33],
            'RSP': [0.33, 0.33, 0.33], 'SRP': [0.33, 0.33, 0.33], 'SPR': [0.33, 0.33, 0.33],
            }
    rps = ['R', 'P', 'S']
    beat = {'P': 'S', 'S': 'R', 'R': 'P'}
    cede = {'P': 'R', 'S': 'P', 'R': 'S'}
    score = {'RR': 0, 'PP': 0, 'SS': 0, 'PR': 1, 'RS': 1, 'SP': 1,'RP': -1, 'SR': -1, 'PS': -1,}
    beatm = defaultdict(lambda: ['R', 'P', 'S'])
    beatm.update({'P': ['S'], 'S': ['R'], 'R': ['P'], 'PR': ['P'], 'RS': ['R'], 'SP': ['S'],'RP': ['P'], 'SR': ['R'], 'PS': ['S'],})
    hist = ""
    patterns = defaultdict(str)
    patterns2 = defaultdict(str)
    output = random.choice(rps)
    csu = [0] * 12 # consecutive strategy usage
    csc = []  # consecutive strategy candidates
    class Neuron:
        def __init__(self, length, learn_factor, initrandom=True):
            self.age = 0
            self.length = length
            self.chooser = ([1] * (length/2)) + ([0] * (length-length/2))

            self.learn_factor = 0.2
            self.unlearn_factor = self.learn_factor / 2

            self.rockweight = [0] * (length+1)
            self.paperweight = [0] * (length+1)
            self.scissorsweight = [0] * (length+1)
            if initrandom:
                v = random.random()
                self.rockweight[random.randint(0,length-1)] = v
                self.rockweight[length] = v / 2

                v = random.random()
                self.paperweight[random.randint(0,length-1)] = v
                self.paperweight[length] = v / 2

                v = random.random()
                self.scissorsweight[random.randint(0,length-1)] = v
                self.scissorsweight[length] = v / 2

        def evaluate(self, neuralinp):
            candidates = []
            net = sum([i*w for i, w in izip(neuralinp, self.rockweight)])
            if net > self.rockweight[-1]:
                candidates.append('R')
            net = sum([i*w for i, w in izip(neuralinp, self.paperweight)])
            if net > self.paperweight[-1]:
                candidates.append('P')
            net = sum([i*w for i, w in izip(neuralinp, self.scissorsweight)])
            if net > self.scissorsweight[-1]:
                candidates.append('S')
            self.candidates = candidates
            return candidates

        def hebbian_learn(self, neuralinp, hand):
            if not neuralinp:
                return
            if hand == 'P':
                self.paperweight = [w+i*self.learn_factor for i, w in izip(neuralinp, self.paperweight)]
            else:
                self.paperweight = [w-i*self.unlearn_factor for i, w in izip(neuralinp, self.paperweight)]

            if hand == 'R':
                self.rockweight = [w+i*self.learn_factor for i, w in izip(neuralinp, self.rockweight)]
            else:
                self.rockweight = [w-i*self.unlearn_factor for i, w in izip(neuralinp, self.rockweight)]

            if hand == 'S':
                self.scissorsweight = [w+i*self.learn_factor for i, w in izip(neuralinp, self.scissorsweight)]
            else:
                self.scissorsweight = [w-i*self.unlearn_factor for i, w in izip(neuralinp, self.scissorsweight)]

    neuralinp = None
    my = opp = my2 = opp2 = ''
    neuron = Neuron(27, 0.3, False)
else:
    print output, input
    neuron.hebbian_learn(neuralinp, input)
    for i, c in enumerate(csc):
        if c == input:
            csu[i] += 1
        else:
            csu[i] = 0

    for i in range(min(len(hist)/2,5), 0, -1):
        pattern = patterns[hist[-i*2:]]
        if pattern:
            for j in range(min(len(pattern)/2,5), 0, -1):
                patterns2[pattern[-2*j]] += output + input
        patterns[hist[-i*2:]] += output + input

    hist += output + input

    my = opp = my2 = opp2 = ''
    for i in range(min(len(hist)/2,5), 0, -1):
        pattern = patterns[hist[-2*i:]]
        if pattern:
            my, opp = pattern[-2:]
            for j in range(min(len(pattern)/2,5), 0, -1):
                pattern2 = patterns2[pattern[-2*j]]
                if pattern2:
                    my2, opp2 = pattern2[-2:]
                    break
            break

    csc = []
    if opp and my:
        csc = [opp, beat[opp], cede[opp], my, cede[my], beat[my]]
    if opp2 and my2:
        csc.extend([opp2, beat[opp2], cede[opp2], my2, cede[my2], beat[my2]])

    m = max(csu)
    switch = "".join(sorted(set([c for i, c in enumerate(csc) if csu[i] == m])))

    neuralinp = split[opp] + split[my] + split[opp2] + split[my2] + split[input] + split[switch]

    neuron.evaluate(neuralinp)

    if neuron.candidates == []:
        neuron.candidates = ['R', 'P', 'S']

    output = random.choice(beatm["".join(neuron.candidates)])