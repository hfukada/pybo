"""
Local gradient-based solver using multiple restarts.
"""

# future imports
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

# global imports
import numpy as np
import scipy.optimize

# local imports
from ...utils import ldsample

# exported symbols
__all__ = ['solve_lbfgs']


def solve_lbfgs(f,
                bounds,
                xx=None,
                ngrid=10000,
                nbest=10,
                rng=None):
    """
    Compute func on a grid, pick nbest points, and LBFGS from there.

    Args:
        f: function handle that takes an optional `grad` boolean kwarg
           and if `grad=True` returns a tuple of `(function, gradient)`.
           NOTE: this functions is assumed to allow for multiple inputs in
           vectorized form.
        bounds: bounds of the search space.
        ngrid: number of (random) grid points to test initially.
        nbest: number of best points from the initial test points to refine.

    Returns:
        xmin, fmin: location and value or minimizer.
    """

    if xx is None:
        # TODO: The following line could be replaced with a regular grid or a
        # Sobol grid.
        xx = ldsample.random(bounds, ngrid, rng)

    # compute func_grad on points xx
    ff = f(xx, grad=False)
    idx_sorted = np.argsort(ff)[::-1]

    # lbfgsb needs the gradient to be "contiguous", squeezing the gradient
    # protects against func_grads that return ndmin=2 arrays
    def objective(x):
        fx, gx = f(x[None], grad=True)
        return -fx[0], -gx[0]

    # TODO: the following can easily be multiprocessed
    result = [scipy.optimize.fmin_l_bfgs_b(objective, x0, bounds=bounds)[:2]
              for x0 in xx[idx_sorted[:nbest]]]

    # loop through the results and pick out the smallest.
    xmin, fmin = result[np.argmin(_[1] for _ in result)]

    # return the values (negate if we're finding a max)
    return xmin, -fmin