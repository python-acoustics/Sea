"""
This module contains abstract base classes from which all components, subsystems, couplings and excitations are ultimately derived of.
The properties these items have in common can be found in these abstract classes.

"""


import math
import cmath
import numpy as np

import warnings # Handling of warnings
import abc      # Abstract base classes
import weakref  # Weak references to objects
import logging  # Add logging functionality

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
    
    _bending_stiffness = None
    
    def _get_bending_stiffness(self):
        if self._bending_stiffness is not None:
            return self._bending_stiffness 
        else: 
            return self.material.young * self.area_moment_of_inertia
    
    def _del_bending_stiffness(self):
        self._bending_stiffness = None
    
    def _set_bending_stiffness(self, x):
        self._bending_stiffness = float(x)
    
    bending_stiffness = property(fget=_get_bending_stiffness, fset=_set_bending_stiffness, fdel=_del_bending_stiffness)
    """
    Bending stiffness :math:`B` is the Young's modulus :math:`E` multiplied with the area moment of inertia :math:`J`.
    
    .. math:: B = E J
    """
    
    
    @property
    def velocity(self):
        """
        Velocity of the component :math:`v_{component}`. This is the sum of all subsystems velocities.
        """
        
        velocity = np.zeros(len(self.omega))
        for subsystem in self.linked_subsystems:
            velocity = velocity + subsystem.velocity()
        return velocity    
        
    
    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        return 20 * np.log10(self.velocity() / (5 * 10**(-8)) ) 
        
        
        
        
class Subsystem(BaseClass):
    """Abstract Base Class for subsystems."""
    __metaclass__ = abc.ABCMeta
    
    linked_couplings_from = list()
    """ 
    List of couplings in which the subsystem is in the From field.
    """

    linked_couplings_to = list()
    """
    List of couplings in which the subsystem is in the To field.
    """
    
    linked_excitations = list()
    """
    List of excitations this subsystem experiences.
    """

    component = None     
    """
    Component this subsystem uses.
    """        
        
    def _set_modal_energy(self, x):
        if len(x) == len(self.omega):
            self._modal_energy = np.array(x)
        
    def _get_modal_energy(self):
        return self._modal_energy
        
    def _del_modal_energy(self):
        self._modal_energy = None

    _modal_energy = None        
    modal_energy = property(_get_modal_energy, _set_modal_energy, _del_modal_energy)
    """
    Modal energies of each frequency band.
    """
        
    
    
    @abc.abstractproperty                      
    def soundspeed_phase(self):
        """
        Phase velocity in a subsystem.
        """
        return
  
    @abc.abstractproperty                      
    def soundspeed_group(self):
        """
        Group velocity in a subsystem.
        """
        return
                
    @abc.abstractproperty
    def modal_density(self):
        """
        Modal density of the subsystem.
        """
        return

    @abc.abstractproperty                      
    def wavenumber(self):
        """
        Wave number.
        """
        return
    
    @abc.abstractproperty
    def mobility(self):
        """
        Acoustic mobility :math:`Y`.
        """
        return
    
    @property
    def input_power(self):
        """
        Total input power due to excitations.
        """
        power = np.zeros(len(self.omega))
        for excitation in self.linked_excitations:
            power = power + excitation.power
        return power    

    @property
    def energy(self):
        """
        Total Energy in subsystem.
        
        .. math:: E = 
        """
        return self.modal_energy * self.modal_density
        
    @property
    def velocity(self):
        """
        Vibrational velocity :math:`v`.
        
        .. math:: v = \\sqrt{\\frac{E}{m}}
        """
        return np.sqrt(self.energy / self.component.mass)
        
    @property
    def velocity_level(self):
        """
        Velocity level.
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        return 20 * np.log10(self.velocity / (5 * 10**(-8)) ) 

class Coupling(BaseClass):
    """Abstract Base Class for couplings."""
    __metaclass__ = abc.ABCMeta
    

    subsystem_from = None
    """
    Subsystem origin for coupling
    """
        
    subsystem_to = None
    """
    Subsystem destination for coupling
    """
    
    @abc.abstractproperty     
    def clf(self):
        """
        Coupling loss factor.
        """
        return   

class Excitation(BaseClass):
    """Abstract Base Class for excitations."""
    __metaclass__ = abc.ABCMeta
        
    subsystem = None
    """
    Subsystem that is being excited by this excitation
    """

    _power = None
    
    def _get_power(self):
        if len(self._power) == len(self.omega):
            return self._power
        else:
            self._power = None
    
    def _set_power(self, x):
        if len(x) == len(self.omega):
            self._power = x
    
    power = property(fget=_get_power, fset=_set_power)
    """
    Input power in watt
    """

class Material(BaseClass):
    """
    Abstract Material Class
    """
    __metaclass__ = abc.ABCMeta
    
    linked_components = None
    """
    Components linked to this subsystem.
    """

    density = 0.0
    """
    Density :math:`\\rho` of the material.
    """
    
    loss_factor = 0.0
    """
    Loss factor :math:`\\eta` of the material.
    """
    
    temperature = 0.0
    """
    Temperature :math:`T`
    """
      
    pressure = 0.0
    """
    Pressure :math:`p`
    """
