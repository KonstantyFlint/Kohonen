from functools import lru_cache
import sys

import matplotlib.pyplot as plt
import numpy as np

from grid import Grid
from plots import plot_sphere
from samples import sample_sphere


def gauss(l):
    @lru_cache(maxsize=None)
    def fun(distance):
        return np.exp(-(distance * distance) / l * l)

    return fun


def time_scale(current_time, max_time):
    return 1 - current_time / max_time


def fit(width: int, height: int, max_time: int, gauss_lambda):
    fig = plt.figure()
    grid = Grid(width, height)
    ax = fig.add_subplot(111, projection='3d')

    plt.show(block=False)

    neighbour_scale_getter = gauss(gauss_lambda)
    for t in range(max_time):
        if (t + 1) % 1000 == 0 or t == max_time - 1:
            print((t + 1) / max_time)
            ax.clear()
            plot_sphere(ax)
            grid.plot(ax)
            plt.pause(0.01)
            plt.draw()
        grid.move(
            sample_getter=sample_sphere,
            neighbour_scale_getter=neighbour_scale_getter,
            time_scale=time_scale(t, max_time),
        )
    plt.show(block=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    args = [int(arg) for arg in args]
    width, height, iterations, gauss_lambda = args
    print(width, height, iterations, gauss_lambda)
    # 30, 30, 30000, 4
    fit(width, height, iterations, gauss_lambda)
