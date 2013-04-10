from ..base import Base

import abc
import math
import cmath
import numpy as np

class Excitation(Base):
    """Abstract Base Class for excitations."""
    __metaclass__ = abc.ABCMeta
        
    subsystem = None
    """
    Subsystem that is being excited by this excitation
    """
    
    object_sort = 'Excitation'

    _power = None
    
    def _get_power(self):
        if len(self._power) == self.frequency.amount:
            return self._power
        else:
            self._power = None
    
    def _set_power(self, x):
        if len(x) == self.frequency.amount:
            self._power = x
    
    power = property(fget=_get_power, fset=_set_power)
    """
    Input power in watt
    """