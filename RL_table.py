import random

# input = ""
nwin = 0
ntie = 0
nloss = 0
iter = 0
epsilon = 0.3
# while True:
preLen = 4
if input == "":
    O = [random.choice('RPS') for i in range(preLen)]
    A = [random.choice('RPS') for i in range(preLen)]
    score = {
        ('R', 'R'): 0, ('R', 'P'): -1, ('R', 'S'): 1,
        ('P', 'R'): 1, ('P', 'P'): 0, ('P', 'S'): -1,
        ('S', 'R'): -1, ('S', 'P'): 1, ('S', 'S'): 0
    }
    Q = dict()
    lr = 0.9
    output = random.choice('RPS')
else:
    input = input.upper()
    state = tuple(O[-preLen:] + A[-preLen:])
    # state = tuple(O[-preLen:])
    action = output
    #    print "program gives: %s" % output
    if score[(output, input)] == 1:
        nloss += 1
    elif score[(output, input)] == 0:
        ntie += 1
    elif score[(output, input)] == -1:
        nwin += 1

    reward = score[(action, input)]
    O.append(input)
    A.append(output)
    newstate = tuple(O[-preLen:] + A[-preLen:])
    # newstate = tuple(O[-preLen:])
    maxvalue = max(Q.get((newstate, a), 0) for a in 'RPS')
    Q[(state, action)] = Q.get((state, action), 0) + lr * (reward + 0.5 * maxvalue - Q.get((state, action), 0))
    succ = [Q.get((newstate, a), 0) for a in 'RPS']
    optimal_actions = ['RPS'[x] for x in range(len(succ)) if succ[x] == max(succ)]
    output = random.choice(optimal_actions) if random.random() > epsilon else random.choice('RPS')
