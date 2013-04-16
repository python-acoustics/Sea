from ..base import Base

import abc
import math
import cmath
import numpy as np

class Component(Base):
    """ Abstract Base Class for components."""
    __metaclass__ = abc.ABCMeta
    
    linked_subsystems = list()
    """ 
    Subsystems that use this component.
    """
    
    material = None
    """
    Material which this component consists of.
    """
    
    volume = None
    """
    Volume :math:`V` of the component.
    """
    
    object_sort = 'Component'
    
    
    @property
    def mass(self):
        """Mass :math:`m` of the component.
        
        :rtype: :class:`float`
        
        .. math:: m = \\rho V 

        """   
        return self.volume * self.material.density
    
        
        

