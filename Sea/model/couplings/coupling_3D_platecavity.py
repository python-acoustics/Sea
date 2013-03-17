import numpy as np
from ..baseclasses import Coupling


class Coupling3DPlateCavity(Coupling):
    
    
    @property
    def impedance_from(self):
        return
    
    @property
    def impedance_to(self):
        return
    
    @property
    def clf(self):
        """
        Coupling loss factor for plate to cavity radiation.
        
        .. math:: \\eta_{plate, cavity} = \\frac{\\rho_0 c_0 \\sigma}{\\omega \\m^{''}}
        
        .. attention::
            Which speed of sound???
        
        See BAC, equation 3.6
        """
        return self.component_from.material.density * self.subsystem_from.soundspeed_group * self.component_from.radiation_efficiency / (self.omega * self.component_from.mass_per_area)
