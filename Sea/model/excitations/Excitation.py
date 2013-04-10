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

    
    power = None
    """
    Input power in watt :class:`numpy.ndarray`
    """