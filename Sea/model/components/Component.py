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
    
    @property
    def velocity(self):
        """Velocity of the component :math:`v_{component}`. 
        
        :rtype: :class:`numpy.ndarray`
        
        This is the sum of all subsystems velocities.       
        """
        
        velocity = np.zeros(self.frequency.amount)
        for subsystem in self.linked_subsystems:
            velocity = velocity + subsystem.velocity
        return velocity    
        
    
    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        try:
            return 20 * np.log10(self.velocity / (5 * 10**(-8)) ) 
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
        

