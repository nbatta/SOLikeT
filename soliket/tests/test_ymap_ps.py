import os
import tempfile

import pytest
import numpy as np

from cobaya.yaml import yaml_load
from cobaya.model import get_model


def get_demo_ymap_ps_model():
    info_yaml = r"""

    likelihood:
      soliket.ymap.ymap_ps.SZLikelihood:


    theory:
      soliket.ymap.ymap_ps.SZForegroundTheory:
        speed: 2



      soliket.ymap.classy_sz:


    params:
      A_CIB:
          prior:
              min: 0
              max: 5
          ref: 0.66
          latex: A_\mathrm{CIB}

      A_RS:
          prior:
              min: 0
              max: 5
          ref: 0.004
          proposal: 0.34
          latex: A_\mathrm{RS}

      A_IR:
          prior:
              min: 0
              max: 5
          ref: 2.04
          proposal: 0.18
          latex: A_\mathrm{IR}

      B:
          prior:
              min: 1.0
              max: 2.0
          ref: 1.4
          proposal: 0.2
          latex: B

      omega_b:
        prior:
          min: 0.02
          max: 0.025
        ref: 0.0224
        proposal: 0.00015
        latex: \Omega_\mathrm{b} h^2

      omega_cdm:
        prior:
          min: 0.11
          max: 0.13
        ref: 0.1202
        proposal: 0.0014
        latex: \Omega_\mathrm{c} h^2

      A_s:
        prior:
          min: 0.1e-9
          max: 10e-9
        ref: 2.1e-9
        proposal: 0.032e-9
        latex: A_\mathrm{s}

      n_s:
        prior:
          min: 0.94
          max: 1.
        ref: 0.965
        proposal: 0.0044
        latex: n_\mathrm{s}

      H0:
        prior:
          min: 55.
          max: 90.
        ref: 67.27
        proposal: 0.6
        latex: H_0
    """

    info = yaml_load(info_yaml)

    # from cobaya.install import install
    # install(info, path=packages_path, skip_global=True)

    test_point = {}

    for par, pdict in info["params"].items():
        # print(pdict)
        if not isinstance(pdict, dict):
            continue

        if "ref" in pdict:
            try:
                value = float(pdict["ref"])
            except TypeError:
                value = (pdict["ref"]["min"] + pdict["ref"]["max"]) / 2
            test_point[par] = value
        elif "prior" in pdict:
            value = (pdict["prior"]["min"] + pdict["prior"]["max"]) / 2
            test_point[par] = value

    model = get_model(info)
    return model, test_point


# @pytest.mark.parametrize("theory", ["camb", "classy"])
def test_ymap_ps():
    model, test_point = get_demo_ymap_ps_model()
    lnl = model.loglike(test_point)[0]
    print('lnl ymap_ps :', lnl)
    assert np.isfinite(lnl)

test_ymap_ps()
