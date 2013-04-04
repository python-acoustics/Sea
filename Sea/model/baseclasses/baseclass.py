import abc
import math
import cmath
import numpy as np

class BaseClass(object):
    """Abstract Base Class for all materials, components, subsystems, couplings and excitations."""
    __metaclass__ = abc.ABCMeta

    system = None
    """
    System of which this object is part.
    """

    frequency = None
    
    @property
    def omega(self):
        """
        Angular frequency
        """
        return self.frequency * 2.0 * np.pi 
        
    
    