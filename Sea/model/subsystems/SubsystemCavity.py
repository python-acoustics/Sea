
import abc
import numpy as np

from Subsystem import Subsystem


class SubsystemCavity(Subsystem): 
    """
    Abstract base class for all Cavity subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
    
    @property
    def wavenumber(self):
        pass
    
    @property
    def soundspeed_group(self):
        """
        Group speed of a fluid in a duct with rigid walls.
        """
        return self.soundspeed_phase
    
    @property
    def soundspeed_phase(self):
        """
        Phase speed of a fluid in a duct with rigid walls.
        
        .. math:: c_0 = c_g = c_{\\phi} = \\sqrt{\\frac{K_0}{\\rho_0}}
        
        See Lyon, above eq 8.1.9.
        """
        try:
            return np.ones(self.frequency.amount) * np.sqrt(self.component.material.bulk / self.component.material.density)
        except ZeroDivisionError:
            return np.zeros(self.frequency.amount)
        
        
