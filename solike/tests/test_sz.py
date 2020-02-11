import pytest
import numpy as np

from cobaya.yaml import yaml_load
from cobaya.model import get_model


def get_demo_sz_model():

    info_yaml = r"""
    likelihood:
        solike.SZLikelihood:
            sim_number: 1
            stop_at_error: True

    theory:
        solike.SZClassy:
            extra_args:
                output: lCl, tCl
        solike.SZForegroundTheory:

    params:
        n_s:
            prior:
              min: 0.8
              max: 1.2
        H0:
            prior:
              min: 40
              max: 100

        my_fg_param_1:
            prior:
                min: 0
                max: 1

        my_fg_param_2:
            prior:
                min: 0
                max: 1

        """

    info = yaml_load(info_yaml)
    model = get_model(info)
    return model


def test_sz():
    model = get_demo_sz_model()
    params = {"n_s": 0.965, "H0": 70, "my_fg_param_1": 0.5, "my_fg_param_2": 0.5}
    lnl = model.loglike(params)[0]

    my_previous_likelihood = -1234.567  # put correct value here

    assert lnl == my_previous_likelihood
