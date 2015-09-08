"""
This demo illustrates how to use pybo to optimize a black-box function
that requires a human in the loop. This script will prompt the user
for a numerical value at a particular design point every time it
needs a new observation.
"""

import matplotlib.pyplot as plt
import numpy as np

from benchfunk.functions import Interactive
from pybo import solve_bayesopt


if __name__ == '__main__':
    # initialize prompter and 1d bounds
    prompter = Interactive()
    bounds = np.array([0., 1.], ndmin=2)

    # define model and optimize
    xbest, model = solve_bayesopt(prompter, bounds, niter=10)

    # visualize
    xx = np.linspace(0, 1, 100)
    yy, s2 = model.predict(xx[:, None])
    s = np.sqrt(s2)
    X, y = model.data
    plt.plot(xx, yy, lw=2)
    plt.fill_between(xx, yy - 2 * s, yy + 2 * s, alpha=0.1)
    plt.scatter(X, y, 50, lw=2, marker='o', facecolor='none')
    plt.show()