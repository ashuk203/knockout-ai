# Time analysis and consistency testing
from game import Knockout
import timeit
import numpy as np

# Note: uncomment lines
#
# 'self._animate = False'
# 'x = lower_spawn_pos + (center / (self._num_penguins - 1)) * (i // 2)'
#
# in game.py before running experiment
if __name__ == '__main__':
    game = Knockout(4, True)
    game2 = Knockout(4, False)

    n = 100
    time_sum = 0
    sqrs = np.zeros((8, 2), dtype=float)
    sums = np.zeros((8, 2), dtype=float)
    game1_sums = np.zeros((8, 2), dtype=float)
    for i in range(n):
        game2 = Knockout(4, "experiment")
        game = Knockout(4, "experiment")

        game.run()
        time_sum += timeit.timeit(game2.run)

        game2_end = np.array(game2.get_positions())
        game1_end = np.array(game.get_positions())

        sums += game2_end
        game1_sums += game1_end

    mean = sums / n
    print("Game 2 stats: ")
    print(time_sum / n)
    print(mean)

    mean_g1 = game1_sums / n
    print("Compare stats: ")
    print(mean_g1)
    print(np.absolute(mean_g1 - mean))
