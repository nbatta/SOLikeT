from cobaya.theory import Theory
from cobaya.classy import Classy
from .gaussian import GaussianLikelihood


class SZClassy(Classy):
    def get_Cl_sz():
        return ...


class SZForegroundTheory(Theory):

    params = {"my_fg_param_1": 1, "my_fg_param_2": 2}

    def calculate(self, state, want_derived=True, **params_values_dict):
        ...
        self.state["Cl_sz_foreground"] = ...


class SZLikelihood(GaussianLikelihood):

    # def initialize(self):
    #     # Do whatever else you may need to do to initialize your special likelihood

    #     super().initialize()

    def get_requirements(self):
        return {"Cl_sz": {}, "Cl_sz_foreground": {}}

    def _get_data(self):
        return ell, Cl_sz

    def _get_cov(self):
        return cov

    def _get_theory(self, **params_values):
        cosmo_params = ...
        foreground_params = ...
        Cl_sz = self.provider.get_Cl_sz(**cosmo_params)
        CL_sz_foreground = self.provider.get_Cl_sz_foreground(**foreground_params)

        return Cl_sz + CL_sz_foreground
