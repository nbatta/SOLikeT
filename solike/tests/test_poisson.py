import numpy as np
import pandas as pd
from functools import partial

from solike.poisson_data import PoissonData

x_min = 0
x_max = 10


def rate_density(x, a):
    """simple linear rate density
    """
    return a * x


def n_expected(a):
    return 0.5 * a * (x_max ** 2 - x_min ** 2)  # integral(rate_density, x_min, x_max)


def generate_data(a):
    # Generate total number
    n = np.random.poisson(n_expected(a))

    # Generate x values according to rate density (normalized as PDF)
    u = np.random.random(n)

    # From inverting CDF of above normalized density
    x = np.sqrt(u * (x_max ** 2 - x_min ** 2) + x_min ** 2)
    return x


def test_poisson_experiment(a_true=3, N=100):
    a_maxlikes = []
    for i in range(N):
        observations = generate_data(a_true)
        catalog = pd.DataFrame({"x": observations})

        data = PoissonData("toy", catalog, ["x"])

        a_grid = np.arange(0.1, 10, 0.2)

        lnl = [data.loglike(partial(rate_density, a=a), n_expected(a)) for a in a_grid]
        a_maxlike = a_grid[np.argmax(lnl)]

        a_maxlikes.append(a_maxlike)

    assert abs(np.mean(a_maxlikes) - a_true) < 0.1