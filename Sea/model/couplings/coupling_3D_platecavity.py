import numpy as np
from ..baseclasses import Coupling


class Coupling3DPlateCavity(Coupling):
    
    
    @property
    def impedance_from(self):
        return self.subsystem_from.impedance
    
    @property
    def impedance_to(self):
        return self.subsystem_to.impedance
    
    @property
    def clf(self):
        """
        Coupling loss factor for plate to cavity radiation.
        
        .. math:: \\eta_{plate, cavity} = \\frac{\\rho_0 c_0 \\sigma}{\\omega \\m^{''}}
        
        .. attention::
            Which speed of sound???
        
        See BAC, equation 3.6
        """
        print self.subsystem_from
        try:
            return self.subsystem_from.component.material.density * self.subsystem_to.soundspeed_group * \
                   self.subsystem_from.radiation_efficiency / (self.omega * self.subsystem_from.component.mass_per_area)
        except ZeroDivisionError:
            return np.zeros(len(self.frequency))