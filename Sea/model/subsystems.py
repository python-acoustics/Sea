"""
Subsystems are the building blocks of an SEA model. Several types of subsystems have been defined.
"""  

import numpy as np
from baseclasses import Subsystem

import abc
 
class SubsystemLong(Subsystem):
    """
    Subsystem for longitudinal waves.
    """

    @property
    def soundspeed_phase(self):
        """
        Phase velocity for longitudinal wave.
        
        .. math:: c_{phase} = \\frac{B}{\\rho}
        """
        return self.component.bending_stiffness / self.component.material.density


    @property
    def soundspeed_group(self):
        """
        Group velocity for longitudinal wave.
        
        .. math:: c_{group} = c_{phase}
        """
        return self.soundspeed_phase

    @property            
    def modal_density(self):
        """
        Modal density for longitudinal waves.
       
        .. math:: \\frac{N}{\\omega} = \\frac{L}{\pi c_L}
        """
        return np.repeat(self.component.length / (np.pi * self.soundspeed_group), len(self.omega))

    @property
    def wavenumber(self):
        """
        Wave number for longitudinal wave.
        """
        return np.sqrt(self.component.density * np.power(self.omega,2) * (1-np.power(self.material.poisson,2)) / (self.component.young * self.component.height))
        
    @property
    def mobility(self):
        return self.component.mobility_long()
    
class SubsystemBend(Subsystem):
    """
    Subsystem for bending waves.
    """

    @property
    def soundspeed_phase(self):
        """
        Phase velocity for bending wave.
        """
        return np.power((np.power(self.omega,2)*self.component.bending_stiffness/self.component.mass_per_area()),0.25)
                
    @property
    def soundspeed_group(self):
        """
        Group velocity for bending wave.
        
        .. math:: c_{group} = 2 c_{phase}
        
        """
        return 2.0 * self.soundspeed_phase()

    @property
    def modal_density(self):
        """
        Modal density for bending waves.
        """
        return self.component.length / (2.0 *np.pi *np.sqrt(self.omega))  * np.power((self.component.mass_per_area/self.component.bending_stiffness),(1/4))
        #return self.component.mass() / (4.0 * np.pi * np.sqrt(self.component.bending_stiffness() * self.component.mass_per_area()))
                
    @property
    def wavenumber(self):
        """
        Wavenumber of bending wave.
        """
        return np.power((self.component.material.density * np.power(self.omega,2) / self.component.bending_stiffness),0.25)
        
    
    @property
    def mobility(self):
        """
        Mobility.
        """
        return self.component.mobility_bend
        
class SubsystemShear(Subsystem):
    """
    Subsystem for shear waves.
    """
    
    @property
    def wavenumber(self):
        """
        Wave number of shear wave.
        """
        return np.sqrt(2.0*self.component.material.density * np.power(self.omega,2) * (1+np.power(poisson,2)) / (self.component.E * self.component.h))
    
    @property
    def mobility(self):
        """
        Mobility.
        """
        return self.component.mobility_shear

     

class SubsystemCavity(Subsystem): 
    """
    Abstract base class for all Cavity subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
    soundspeed = None
    """
    Sound speed for longitudinal waves in a fluid.
    
    .. math:: c_{group} = c_{phase}
    
    """
    
    @property
    def soundspeed_phase(self):
        """
        Phase speed for longitudinal waves in a fluid.
        """
        return self.soundspeed
    
    @property
    def soundspeed_group(self):
        """
        Group speed for longitudinal waves in a fluid.
        """
        return self.soundspeed
        
        
class SubsystemCavity2D(SubsystemCavity):
    """
    Subsystem for a 2D room.
    """
    pass
    
class SubsystemCavity3D(SubsystemCavity):
    """
    Subsystem for a 3D room.
    """
    pass
    

