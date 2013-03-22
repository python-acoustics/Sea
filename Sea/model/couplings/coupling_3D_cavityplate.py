import numpy as np
from ..baseclasses import Coupling



class Coupling3DCavityPlate(Coupling):
    
    
    @property
    def impedance_from(self):
        return self.subsystem_from.impedance
    
    @property
    def impedance_to(self):
        return self.subsystem_to.impedance
    
    
    @property
    def clf(self):
        """
        Coupling loss factor for transmission from a cavity to a plate.
        
        .. math:: \\eta_{cavity,plate} = \\frac{\\rho_0 c^2 S \\sigma f_c }{8 \\pi f^3 m^{''} V_2}
        
        See BAC, equation 3.9
        """
        print self.component_to
        print self.subsystem_to
        
        try:
            return self.subsystem_from.component.material.density * \
                   self.subsystem_from.soundspeed_group**2.0 *self.area * self.subsystem_to.radiation_efficiency * \
                   self.subsystem_to.critical_frequency / (8.0 * np.pi * self.frequency**3.0 * \
                   self.subsystem_to.component.mass_per_area * self.subsystem_from.component.volume) 
        except ZeroDivisionError:
            return np.zeros(len(self.frequency))

        
        