"""
This module contains abstract base classes from which all components, subsystems, couplings and excitations are ultimately derived of.
The properties these items have in common can be found in these abstract classes.
"""

import math
import cmath
import numpy as np

import warnings # Handling of warnings
import abc      # Abstract base classes
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
        
        
        
        
class ComponentStructural(Component):
    """
    Abstract base class for structural components.
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

class ComponentCavity(Component):
    """
    Abstract base class for fluid components.
    """
    pass
        
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


    def __init__(self, component):
        """
        Constructor
        
        :param component: Component this object belongs to.
        """
        
        
        self.component = component
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
    def average_frequency_spacing(self):
        """"
        Average frequency spacing.
        """
        return
    
    @property            
    def modal_density(self):
        """
        Modal density.
       
        .. math:: n(\\omega) = \\frac{1}{2 \\pi \\overline{\\delta f}}
        
        See Lyon, eq. 8.1.6
        """
        return 1.0 / (2.0 * np.pi * self.average_frequency_spacing)

    #@abc.abstractproperty                      
    #def wavenumber(self):
        #"""
        #Wave number.
        #"""
        #return
    
    #@abc.abstractproperty
    @property
    def impedance(self):
        """
        Impedance `Z`
        """
        return
        
    
    @property
    def resistance(self):
        """
        Resistance `R`, the real part of the impedance `Z`
        """
        return np.real(self.impedance)
    
    @property
    def mobility(self):
        """
        Mobility `Y`
        """
        return 1.0 / self.impedance
    
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


        
class SubsystemStructural(Subsystem):
    """
    Abstract base class for all Structural subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    pass
    
class SubsystemCavity(Subsystem): 
    """
    Abstract base class for all Cavity subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
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
        return np.sqrt(self.component.material.bulk_modulus / self.component.material.density)

        
        
class Coupling(BaseClass):
    """Abstract Base Class for couplings."""
    __metaclass__ = abc.ABCMeta
    
    components = list()
    """
    List of all components that connect to this coupling."""
    
    subsystems = list()
    """List of all enabled subsystems that make use of this coupling."""
    
    @abc.abstractproperty
    def impedance(self):
        """
        Impedance of the coupling is the sum of the impedances of all subsystems.
        """
        return
    
    @abc.abstractproperty
    def clf(self, subsystem_from, subsystem_to):
        """
        Coupling loss factor `\\eta`.
        """
        return
        
        
class CouplingOld(BaseClass):
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
