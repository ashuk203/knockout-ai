
from game import Player
from game import step
import scipy.optimize
import numpy as np
def score(p1,p2):
    s = 0
    for p in p1.ps:
        s += (400 - p[0]) * p[0]
        s += (400 - p[1]) * p[1]
    for p in p2.ps:
        s -= (400 - p[0]) * p[0]
        s -= (400 - p[1]) * p[1]
    return -s

def strategyScore(Velocities,p1, p2):
    p1 = p1.copy()
    p2 = p2.copy()
    for i in range(len(Velocities)):
        if i%2 == 0:
            p1.vs[i//2]=(Velocities[i], Velocities[i] + 1)

    p1, p2 = step(p1, p2)
    return score(p1, p2)


def bestStrategy(p1, p2):
    v = scipy.optimize.minimize(lambda v: strategyScore(v, p1, p2),
                            x0 = np.array([p1.vs[i//2][i%2] for i in range(len(p1.vs) * 2)]),
                            method = 'powell'
                            #,bounds = [(-400, 400) for i in range(len(p1.vs)*2)]
                            )
    for i in range(len(v.x)):
        if i % 2 == 0:
            p1.vs[i // 2] = (v.x[i], v.x[i] + 1)
    return p1, p2

def bestStrategyIteration(n, p1, p2):
    for i in range(n):
        p1, p2 = bestStrategy(p1, p2)
        p2, p1 = bestStrategy(p2, p1)

if __name__ == '__main__':
    p1 = Player()
    p1.ps.append((50,50))
    p1.vs.append((100,100))
    p2 = Player()
    p2.ps.append((100, 100))
    p2.vs.append((-100, -100))
    for i in range(20):
        bestStrategyIteration(5, p1, p2)
        p1, p2 = step(p1, p2)
        print(p1.ps, p2.ps)
