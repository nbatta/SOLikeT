from collections import ChainMap

import numpy as np

from cobaya.likelihood import Likelihood
from cobaya.input import merge_info, merge_params_info
from cobaya.tools import recursive_update

from .gaussian_data import GaussianData, MultiGaussianData
from .utils import get_likelihood


class GaussianLikelihood(Likelihood):

    class_options = {
        "name": "Gaussian",
        "datapath": None,
        "covpath": None,
    }

    def initialize(self):
        x, y = self._get_data()
        cov = self._get_cov()
        self.data = GaussianData(self.name, x, y, cov)

    def _get_data(self):
        x, y = np.loadtxt(self.datapath, unpack=True)
        return x, y

    def _get_cov(self):
        cov = np.loadtxt(self.covpath)
        return cov

    def _get_theory(self, **kwargs):
        raise NotImplementedError

    def logp(self, **params_values):
        theory = self._get_theory(**params_values)
        return self.data.loglike(theory)


class CrossCov(dict):
    def save(self, path):
        np.savez(path, **{str(k): v for k, v in self.items()})

    @classmethod
    def load(cls, path):
        if path is None:
            return None
        return cls({eval(k): v for k, v in np.load(path).items()})


class MultiGaussianLikelihood(GaussianLikelihood):
    class_options = {"components": None, "options": None, "cross_cov_path": None}

    def initialize(self):
        self.likelihoods = [get_likelihood(*kv) for kv in zip(self.components, self.options)]

        self.cross_cov = CrossCov.load(self.cross_cov_path)

        # Why doesn't merge_params_info() work here?
        all_params = [l.params for l in self.likelihoods if hasattr(l, "params")]
        if all_params:
            self.params = merge_info(*all_params)

        data_list = [l.data for l in self.likelihoods]
        self.data = MultiGaussianData(data_list, self.cross_cov)

    def initialize_with_provider(self, provider):
        for like in self.likelihoods:
            like.initialize_with_provider(provider)
        super().initialize_with_provider(provider)

    def _get_theory(self, **kwargs):
        return np.concatenate([l._get_theory(**kwargs) for l in self.likelihoods])

    def get_requirements(self):
        reqs = {}
        for like in self.likelihoods:
            reqs = recursive_update(reqs, like.get_requirements())
        return reqs
        # return merge_info(*[l.get_requirements() for l in self.likelihoods])
