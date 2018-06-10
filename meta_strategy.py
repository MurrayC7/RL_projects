###############################################################################
#                                                                             #
# This is AmateurSwordsman, an RPS program written by PotentProton.           #
#                                                                             #
# This program is a simplification of the program Swordsman. It consists of   #
# two parts.                                                                  #
#                                                                             #
# In the first part, Swordsman tries to match the most recent moves within    #
# the full history of both players' moves. Longer matches are prioritized, as #
# are more recent matches. When a match is found, we assume that the next     #
# move will be the same as the last time this matched sequence of moves       #
# occurred.                                                                   #
#                                                                             #
# In the second part, we apply a meta-strategy. This helps to protect against #
# opponents who might detect that we are using this strategy, and then be     #
# able to accurately predict our moves because of this. If we rotate our      #
# guess (R->P,P->S,S->R) we can escape from this situation.                   #
#                                                                             #
# If we track the expected score per turn of each meta-strategy (add 1 when   #
# it wins, subtract one when it loses), we can get a good idea of which one   #
# will be most successful. However, we also care more about recent results,   #
# because we need to be reacting to what are opponent is doing right now      #
# (they can switch between meta-strategies also). We therefore remove weight  #
# from older results, to make them less significant.                          #
#                                                                             #
# Unlike the Swordsman program, this program does not use mirroring. My hope  #
# is that this achieves better performance against weaker opponents, with     #
# cost in reduced effectiveness against a very small number of stronger       #
# opponents. For a weaker opponent, trying to guess what they may do if they  #
# were pattern-matching against our own moves probably is not useful, and may #
# add noise which makes it difficult to find patterns in their moves.         #
#                                                                             #
# I have also changed the length of history that the program tries to match.  #
# Swordsman tries to match the entire history, which against a simple         #
# program, such as one that always plays rock, can result in matching 999     #
# moves. This is excessive. I have limited the length of history to match to  #
# be less than 15. In trial runs this seems to not leave any degradation in   #
# performance.                                                                #
#                                                                             #
###############################################################################

import random

if input == "":
    ##################################################
    # Create read-only useful conversion structures. #
    ##################################################

    # Convert input+output pair to shorthand:
    iop2sh = {'RR': '0', 'RP': '1', 'RS': '2', 'PR': '3', 'PP': '4', 'PS': '5', 'SR': '6', 'SP': '7', 'SS': '8'}
    # Get input from shorthand:
    sh2i = {'0': 'R', '1': 'R', '2': 'R', '3': 'P', '4': 'P', '5': 'P', '6': 'S', '7': 'S', '8': 'S'}
    # Get output from shorthand:
    sh2o = {'0': 'R', '1': 'P', '2': 'S', '3': 'R', '4': 'P', '5': 'S', '6': 'R', '7': 'P', '8': 'S'}

    # Get move that beats given move:
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}
    # Get move that loses to given move:
    lose = {'R': 'S', 'P': 'R', 'S': 'P'}

    ####################################
    # Initialize more data structures. #
    ####################################

    # Move history, for analysis:
    hist = ''

    # Current move number:
    now = 0

    # Output selections and scores for meta strategies:
    mo = ['X'] * 3
    msc = [0.0] * 3

    ################
    # Select move. #
    ################

    # Since we have no data to go on, we use randomness.
    output = random.choice(['R', 'P', 'S'])
else:
    ####################
    # Update raw data. #
    ####################

    # Record most recent input output pair:
    hist += iop2sh[input + output]

    # Increment the move number:
    now += 1

    # Update meta strategy scores. We add a decay multiplier of 0.9 to give
    # more weight to more recent events.
    for i in xrange(0, len(mo)):
        # Check that there has actually been a prediction.
        if mo[i] != 'X':
            if mo[i] == beat[input]:
                msc[i] += 1.0
            elif mo[i] == lose[input]:
                msc[i] -= 1.0
            msc[i] *= 0.9

    #######################
    # Do pattern matching #
    #######################

    # We search for a sequence of events in the history which matches recent
    # events. We try to match longer and longer strings until we fail. The
    # Python rfind function starts at the end of the list and searches
    # backwards, giving us the most recent occurrence of a sequence. Note that
    # the for loop will not run if now < 2.
    match = -1
    for i in xrange(1, min(15, now - 1)):
        localmatch = hist[:(now - 1)].rfind(hist[-i:])
        if localmatch != -1:
            # match was found, update with the new best match.
            match = localmatch + i
        else:
            # no reason to continue, next iteration is strictly harder to
            # match.
            break

    if match == -1:
        # No match could be found, so we pick a random output.
        output = random.choice(['R', 'P', 'S'])
        # Also reset the meta moves so that we don't rescore moves twice.
        mo = ['X'] * 3
    else:
        # Get shorthand of match from history.
        shmatch = hist[match]
        # Get input/output from shorthand of match.
        imatch = sh2i[shmatch]

        ###########################################
        # Select output using best meta strategy. #
        ###########################################

        # Select outputs desired by different strategies.
        mo[0] = imatch
        mo[1] = beat[imatch]
        mo[2] = lose[imatch]

        # Find strategy with highest expected value.
        maxmo = 'X'  # Output of best meta-strategy.
        maxmsc = -1001  # Score of best meta-strategy.
        maxvalid = 0  # Maximum invalidated in case of conflicting tie.
        for i in xrange(0, len(mo)):
            if msc[i] > maxmsc:
                maxmo = mo[i]
                maxmsc = msc[i]
                maxvalid = 1
            elif (msc[i] == maxmsc) and (mo[i] != maxmo):
                # In the case of a tie between meta strategies, and the meta
                # strategies select different outputs, we should pick a random
                # output instead.
                maxvalid = 0

        if maxvalid:
            output = maxmo
        else:
            # Picking random output because of meta strategy tie.
            output = random.choice(['R', 'P', 'S'])