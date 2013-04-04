from baseclass import BaseClass

import abc
import math
import cmath
import numpy as np

class Component(BaseClass):
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
    
    def _get_mass(self):
        if self._mass == None:
            return self.volume * self.material.density
    
    def _set_mass(self, x):
        self._mass = x
    

    _mass = None
    mass = property(fget=_get_mass, fset=_set_mass)
    """
    Mass :math:`m` of the component.
    
    .. math:: m = \\rho V 
    
    """   
    
    @property
    def velocity(self):
        """
        Velocity of the component :math:`v_{component}`. This is the sum of all subsystems velocities.
        """
        
        velocity = np.zeros(len(self.omega))
        for subsystem in self.linked_subsystems:
            velocity = velocity + subsystem.velocity
        return velocity    
        
    
    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        try:
            return 20 * np.log10(self.velocity / (5 * 10**(-8)) ) 
        except FloatingPointError:
            return np.zeros(len(self.frequency))
        

class ComponentStructural(Component):
    """
    Abstract base class for structural components.
    """
    availableSubsystems = ['Long', 'Bend', 'Shear']
    

class ComponentCavity(Component):
    """
    Abstract base class for fluid components.
    """
    
    availableSubsystems = ['Long']
