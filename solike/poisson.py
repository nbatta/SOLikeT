import pandas as pd

from cobaya.likelihood import Likelihood

from .poisson_data import PoissonData


class PoissonLikelihood(Likelihood):
    class_options = {"name": "Poisson", "catalog_path": None, "columns": None}

    def initialize(self):
        catalog = self._get_catalog()
        if self.columns is None:
            self.columns = catalog.columns
        self.data = PoissonData(self.name, catalog, self.columns)

    def _get_catalog(self):
        return pd.read_csv(self.catalog_path)

    def _get_rate_fn(self, **kwargs):
        """Returns a callable rate function that takes each of 'columns' as kwargs.
        """
        raise NotImplementedError

    def _get_n_expected(self, **kwargs):
        """Computes and returns the integral of the rate function 
        """
        raise NotImplementedError

    def logp(self, **params_values):
        rate_fn = self._get_rate_fn(**params_values)
        n_expected = self._get_n_expected(**params_values)
        return self.data.loglike(rate_fn, n_expected)
