from baseclass import BaseClass

import abc
import math
import cmath
import numpy as np

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
    
    object_sort = 'Coupling'
    
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
        return self.frequency.center * self.clf / self.subsystem_from.average_frequency_spacing
        
