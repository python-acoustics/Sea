import numpy as np
from ..baseclasses import Coupling
    
class Coupling2DStructural(Coupling):
    

    @property
    def impedance_from(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """
        if self.subsystem_from.impedance:
            return self.subsystem_from.impedance
        else:
            return np.zeros(len(self.frequency))
            
    @property
    def impedance_to(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """     
        if self.subsystem_to.impedance:
            return self.subsystem_to.impedance
        else:
            return np.zeros(len(self.frequency))
            
    
    
    @property
    def clf(self):
        return 0.5