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
    availableSubsystems = ['Long', 'Bend', 'Shear']
    

class ComponentCavity(Component):
    """
    Abstract base class for fluid components.
    """
    
    availableSubsystems = ['Long']
        
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
    
    def _set_modal_overlap_factor(self, x):
        self._modal_overlap_factor = x
    
    def _get_modal_overlap_factor(self):
        if not self._modal_overlap_factor:
            return self.component.material.loss_factor
        else:
            self._modal_overlap_factor
    
    _modal_overlap_factor = None
    modal_overlap_factor = property(fget=_get_modal_overlap_factor, fset=_set_modal_overlap_factor)
    """
    Modal overlap factor. Initial value is based on damping loss factor of subsystem.
    After solving the system a first time, this value is updated to its results.
    This value is iteratively updated.
    """
    
    @property
    def clf(self):
        return np.zeros(len(self.frequency))
    
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
        try:
            return 1.0 / (2.0 * np.pi * self.average_frequency_spacing)
        except FloatingPointError:
            return np.zeros(len(self.frequency))
        
    #@abc.abstractproperty                      
    #def wavenumber(self):
        #"""
        #Wave number.
        #"""
        #return
    
    @property
    def impedance(self):
        """
        Impedance `Z`
        """
        return
        
    
    @property
    def resistance(self):
        """
        Resistance `R`, the real part of the impedance `Z`.
        
        .. math:: R = \\Re{Z}
        """
        return np.real(self.impedance)
    
    @property
    def mobility(self):
        """
        Mobility `Y`
        
        .. math:: Y = \\frac{1}{Z}
        """
        try:
            return 1.0 / self.impedance
        except FloatingPointError:
            return np.zeros(len(self.frequency))
            
    @property
    def damping_term(self):
        """
        The damping term is the ratio of the modal half-power bandwidth to the average modal frequency spacing.
        
        .. math:: \\beta_{ii} = \\frac{f \\eta_{loss} }{\\overline{\\delta f}}
        
        See Lyon, above equation 12.1.4
        """
        try:
            return self.frequency * self.component.material.loss_factor / self.average_frequency_spacing
        except FloatingPointError:
            return np.zeros(len(self.frequency))
        
    @property
    def modal_overlap_factor(self):
        """
        Modal overlap factor.
        
        .. math:: M = \\frac{ \\pi \\beta_{ii} }{2}
        
        See Lyon, above equation 12.1.4
        """
        return np.pi * self.damping_term / 2.0
    
    
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
        try:
            return np.sqrt(self.energy / self.component.mass)
        except FloatingPointError:
            return np.zeros(len(self.frequency))
            
    @property
    def velocity_level(self):
        """
        Velocity level.
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        try:
            return 20 * np.log10(self.velocity / (5 * 10**(-8)) ) 
        except FloatingPointError:
            return np.zeros(len(self.frequency))
    
        
class SubsystemStructural(Subsystem):
    """
    Abstract base class for all Structural subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
    #@property
    #def radiation_efficiency(self):
        #return np.zeros(len(self.frequency))
    
    #@property
    #def critical_frequency(self):
        #return 0.0
    
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
            return np.ones(len(self.frequency)) * np.sqrt(self.component.material.bulk / self.component.material.density)
        except ZeroDivisionError:
            return np.zeros(len(self.frequency))
        
        

class Coupling(BaseClass):
    """
    Abstract base class for couplings.
    """
    __metaclass__ = abc.ABCMeta
    
    
    connection = None
    """
    Connection this coupling is part of.
    """
    
    
    component_from = None
    """
    Component
    """
    component_to = None
    """
    Component
    """
    subsystem_from = None
    """
    Type of subsystem origin for coupling
    """
    subsystem_to = None
    """
    Type of subsystem destination for coupling
    """
    
    size = None
    """
    Size of the coupling.
    """
    
    @abc.abstractproperty
    def impedance_from(self):
        """
        Impedance of :attr:`subsystem_from` corrected for the type of coupling.
        """
        return
    
    @abc.abstractproperty
    def impedance_to(self):
        """
        Impedance of :attr:`subsystem_to` corrected for the type of coupling.
        """
        return
     
    @abc.abstractproperty
    def clf(self):
        """
        Coupling loss factor `\\eta`.
        """
        return
        
    @property
    def mobility_from(self):
        """
        Mobility of :attr:`subsystem_from` corrected for the type of coupling.
        """
        return 1.0 / self.impedance_from
        
    @property
    def mobility_to(self):
        """
        Mobility of :attr:`subsystem_to` corrected for the type of coupling.
        """
        return 1.0 / self.impedance_to
    
    @property
    def resistance_from(self):
        """
        Resistance of :attr:`subsystem_from` corrected for the type of coupling.
        """
        return np.real(self.impedance_from)
    
    @property
    def resistance_to(self):
        """
        Resistance of :attr:`subsystem_to` corrected for the type of coupling.
        """
        return np.real(self.impedance_to)
    
    
    @property
    def modal_coupling_factor(self):
        """
        Modal coupling factor of the coupling.
        
        .. math:: \\beta_{ij} = \\frac{ f * \\eta_{ij} } { \\overline{\\delta f_i} }
        
        See Lyon, above equation 12.1.4
        """
        return self.frequency * self.clf / self.subsystem_from.average_frequency_spacing
        

        
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

    bulk = 0.0
    """
    Bulk modulus
    """