
from game import Player
from game import step
import scipy.optimize
import numpy as np

def printp(p1,p2):
    p1 = p1.copy()
    p2 = p2.copy()
    p1, p2 = step(p1, p2)
    print(p1.ps, p2.ps)
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
    s = 0
    for i in range(len(Velocities)):
        s += Velocities[i]**2
        if i%2 == 0:
            p1.vs[i//2]=(Velocities[i], Velocities[i+1])

    p1, p2 = step(p1, p2)
    return score(p1, p2) - s

def kpastStrategyScore(Velocities,p1, p2s, falloff=1):
    p1 = p1.copy()
    for i in range(len(Velocities)):
        if i%2 == 0:
            p1.vs[i//2]=(Velocities[i], Velocities[i+1])
    f = 1
    s = 0
    for p2 in p2s:
        p2 = p2.copy()
        p1, p2 = step(p1, p2)
        ns = f * score(p1, p2)
        s += ns
        f *= falloff
    return s


def bestStrategy(p1, p2):
    v = scipy.optimize.minimize(lambda v: strategyScore(v, p1, p2),
                            x0 = np.array([p1.vs[i//2][i%2] for i in range(len(p1.vs) * 2)]),
                            method = 'powell'
                            #,bounds = [(-400, 400) for i in range(len(p1.vs)*2)]
                            )
    for i in range(len(v.x)):
        if i % 2 == 0:
            p1.vs[i // 2] = (v.x[i], v.x[i+1])
    return p1, p2

def kpastBestStrategy(p1, p2s):
    v = scipy.optimize.minimize(lambda v: kpastStrategyScore(v, p1, p2s),
                            x0 = 100*np.random.rand((len(p1.vs)*2)) - 50,#np.array([p1.vs[i//2][i%2] for i in range(len(p1.vs) * 2)]),
                            method = 'powell'
                            ,bounds = [(-400, 400) for i in range(len(p1.vs)*2)]
                            )
    print(kpastStrategyScore(v.x, p1, p2s, falloff=1))
    for i in range(len(v.x)):
        if i % 2 == 0:
            p1.vs[i // 2] = (v.x[i], v.x[i+1])
    return p1, p2s[0]

def bestStrategyIteration(n, p1, p2):
    for i in range(n):
        p1, p2 = bestStrategy(p1, p2)
        p2, p1 = bestStrategy(p2, p1)



def kpastBestStrategyIteration(n, p1, p2, k):
    p2s = [p2.copy() for i in range(k)]
    p1s = [p1.copy() for i in range(k)]
    for i in range(k):
        for j in range(len(p2s[i].vs)):
            p2s[i].vs[j] = (100 * np.cos(2*np.pi*i/k), (100 * np.sin(2*np.pi*i/k)))
            p1s[i].vs[j] = (100 * np.cos(2 * np.pi * i / k), (100 * np.sin(2 * np.pi * i / k)))

    for i in range(n):
        print(n)
        p1, p2 = kpastBestStrategy(p1.copy(), p2s)
        p1s.insert(0, p1.copy())
        if len(p1s) > k:
            p1s.pop(-1)
        p2, p1 = kpastBestStrategy(p2.copy(), p1s)
        p2s.insert(0, p2.copy())
        if len(p2s) > k:
            p2s.pop(-1)
    return p1s[0], p2s[0]

def recBuildDescretized(p1, p2, minPower, maxPower, s, i):
    if i < len(p1.ps):
        ret = []
        for x in range(minPower, maxPower, s):
            for y in range(minPower, maxPower, s):
                p1.vs[i] = (x,y)
                ret.append(recBuildDescretized(p1, p2, minPower, maxPower, s, i+ 1))

        return ret

    i -= len(p1.ps)
    if i < len(p2.ps):
        ret = []
        for x in range(minPower, maxPower, s):
            for y in range(minPower, maxPower, s):
                p2.vs[i] = (x, y)
                ret.append(recBuildDescretized(p1, p2, minPower, maxPower, s, i + len(p1.ps)+ 1))
        return ret

    return strategyScore([],p1, p2)

def buildDescretized(p1, p2, minPower, maxPower, s):
    return np.array(recBuildDescretized(p1, p2, minPower, maxPower, s, 0))

if __name__ == '__main__':
    p1 = Player()
    p1.ps.append((100,200))
    p1.vs.append((100,100))
    p2 = Player()
    p2.ps.append((300, 200))
    p2.vs.append((-100, -100))
    #print(buildDescretized(p1,p2,-100, 100, 100))
    for i in range(20):
         p1,p2 = kpastBestStrategyIteration(100, p1, p2, 20)
         p1, p2 = step(p1, p2, show = True)
         print(p1.ps, p2.ps)

