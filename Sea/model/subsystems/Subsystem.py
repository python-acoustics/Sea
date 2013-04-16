from ..base import Base

import abc
import math
import cmath
import numpy as np

class Subsystem(Base):
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

    object_sort = 'Subsystem'
        
    component = None
    """
    Component this subsystem uses.
    """        
    
    modal_energy = None        
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
        return np.zeros(self.frequency.amount)
    
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
            return np.zeros(self.frequency.amount)
        
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
            return np.zeros(self.frequency.amount)
            
    @property
    def damping_term(self):
        """
        The damping term is the ratio of the modal half-power bandwidth to the average modal frequency spacing.
        
        .. math:: \\beta_{ii} = \\frac{f \\eta_{loss} }{\\overline{\\delta f}}
        
        See Lyon, above equation 12.1.4
        """
        try:
            return self.frequency.center * self.component.material.loss_factor / self.average_frequency_spacing
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
        
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
        power = np.zeros(self.frequency.amount)
        #print self.linked_excitations
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
        
        