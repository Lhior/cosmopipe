import numpy as np

from cosmopipe.lib import theory
from cosmopipe.lib.theory.base import ProjectionBase, BaseModel, ModelCollection
from cosmopipe.lib.modules import ParameterizedModule

from cosmopipe import section_names


class BasicModel(ParameterizedModule):

    def setup(self):
        # this adds parameters defined in basic_model.yaml to the ParamBlock
        self.set_param_block()
        # here we declare what this model is about, let's say it is just the monopole of the power spectrum, reliable between 1e-4 et 100 h/Mpc
        base = ProjectionBase(x=np.linspace(1e-4,100,100),space=ProjectionBase.POWER,mode=ProjectionBase.MULTIPOLE,projs=[0])
        # a model = a function (callable) (None for now, it will be given in execute()) + a ProjectionBase
        self.model = BaseModel(base=base)
        # we add the model to the model collection of self.data_block[section_names.model,'collection'], passed on to other modules
        self.data_block[section_names.model,'collection'] = self.data_block.get(section_names.model,'collection',[]) + ModelCollection([self.model])

    def execute(self):
        # we retrieve the bias
        b = self.data_block[section_names.galaxy_bias,'b']

        def model(k):
            return b * np.ones((k.size,1),dtype='f8')

        # we monkey-patch our current function to the model instance
        self.model.eval = model

        self.data_block[section_names.model,'collection'] = self.data_block.get(section_names.model,'collection',[]) + ModelCollection([self.model])

    def cleanup(self):
        pass
