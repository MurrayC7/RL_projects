# added random fallback to dumbneurals-v0.1

if input == "":
    import random
    import math


    class NN(object):
        learnrate = {"win": 0.01, "tie": 0.2, "loss": 0.5}

        def __init__(self, ins):
            # number of nodes
            self.ni = ins
            self.no = 3
            # init activations
            self.ia = [0] * self.ni
            self.oa = [0] * self.no
            # init weights
            # initial weights need(?) to be below 3/self.ni
            self.weights = [[random.uniform(0, 3. / self.ni) for i in range(self.ni)]
                            for j in range(self.no)]

        def feed(self, inps):
            self.ia = inps
            self.oa = [sum(self.weights[j][i] * self.ia[i]
                           for i in range(self.ni))
                       for j in range(self.no)]
            return self.oa

        def train(self, target, last_round):
            # hebb learning rule
            # factor of 1/self.ni*3 is there to ensure output
            # in range 0,1 if lernrates are < 1
            # and inputs are 1 for every third inputnode
            # maybe important for convergence?
            result_last_round = result[last_round]
            learnrate = self.learnrate[result_last_round]
            error = map(lambda x, y: x - y, target, self.oa)
            for i in range(self.ni):
                for j in range(self.no):
                    self.weights[j][i] += (learnrate * error[j] * self.ia[i] /
                                           self.ni * 3)


    result = {"RS": "win", "SP": "win", "PR": "win",
              "RR": "tie", "SS": "tie", "PP": "tie",
              "SR": "loss", "PS": "loss", "RP": "loss"}
    num_moves = 5  # number of recent rounds the neurons get to see
    nn = NN(num_moves * 6)
    ourmoves = ""
    oppmoves = ""
    nnpred = "S"
    round_cnt = 0
    score = 0
    scores = {"win": 1, "tie": 0, "loss": -1}


    def moves_to_repr(moves):
        repr_lookup = {"R": [1, 0, 0], "S": [0, 1, 0], "P": [0, 0, 1]}
        nninput = []
        for c in moves:
            nninput.extend(repr_lookup[c])
        return nninput


    def repr_to_move(nnoutput):
        ciphers = "RSP"
        index = max(enumerate(nnoutput), key=lambda x: x[1])[0]
        return ciphers[index]


    def feedneurons():
        inps = moves_to_repr(ourmoves[-num_moves:] + oppmoves[-num_moves:])
        ourmove = nn.feed(inps)
        return repr_to_move(ourmove)


    def trainneurons(nn_last_round):
        win = dict(zip("RSP", "PRS"))
        target = moves_to_repr(win[oppmoves[-1]])
        nn.train(target, nn_last_round)


    output = random.choice("RSP")
    ourmoves += output
else:
    oppmoves += input
    round_cnt += 1
    if round_cnt < 5:
        output = random.choice("RSP")
    else:
        nn_last_round = nnpred + oppmoves[-1]
        trainneurons(nn_last_round)
        score = 0.9 * score + scores[result[nn_last_round]]
        nnpred = feedneurons()
        if score > 0.5:  # do we have confidence?
            output = nnpred
        else:  # fall back if we cannot beat you
            output = random.choice("RSP")
    ourmoves += output