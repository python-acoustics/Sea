import numpy as np
from ..baseclasses import Coupling
    
class Coupling2DStructural(Coupling):
    

    @property
    def impedance_from(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """
        return subsystem_from.impedance

    @property
    def impedance_to(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """     
        return subsystem_to.impedance
    
    
    
    @property
    def clf(self):
        pass