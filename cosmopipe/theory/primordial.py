import numpy as np

from cosmopipe.lib.primordial import Cosmology
from cosmopipe import section_names


class Primordial(object):

    def setup(self):
        self.compute = self.options.get('compute',[])
        self.calculation_params = {}
        self.calculation_params['engine'] = self.options.get('engine','class')
        for name,value in Cosmology.get_default_parameters(of='calculation',include_conflicts=True).items():
            self.calculation_params[name] = self.options.get(name,value)
        self.optional_params = Cosmology.get_default_parameters(of='cosmology')

    def execute(self):
        kwargs = {}
        for par in self.optional_params:
            try:
                kwargs[par] = self.data_block.get(section_names.cosmological_parameters,par)
            except KeyError:
                pass
        cosmo = Cosmology(**kwargs,**self.calculation_params)
        self.data_block[section_names.primordial_cosmology,'cosmo'] = cosmo
        fo = cosmo.get_fourier()
        if 'pk_m' in self.compute:
            self.data_block[section_names.primordial_perturbations,'pk_callable'] = fo.pk_interpolator(of='delta_m')
        if 'pk_cb' in self.compute:
            self.data_block[section_names.primordial_perturbations,'pk_callable'] = fo.pk_interpolator(of='delta_cb')

    def cleanup(self):
        pass