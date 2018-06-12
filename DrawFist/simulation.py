import numpy as np


def simulate(mode):
    if mode == 'Gaussian':
        x = 0.5 * np.random.randn(36) + 0.5
        has_neg = False
        for neg in x < 0:
            if neg:
                has_neg = True
        if has_neg:
            x = x - 1.5 * np.min(x)
        y = np.sum(x)
        return x / y
    else:
        return 0
