"""
This module contains a class to describe physical connections between :mod:`Sea.model.components`.
"""
import math
import cmath
import numpy as np

import warnings # Handling of warnings
import abc      # Abstract base classes
import logging  # Add logging functionality

from baseclasses import BaseClass

class Connection(BaseClass):
    """Class for connections between components."""
    #__metaclass__ = abc.ABCMeta
    
    components = list()
    """
    List of components that are connected through this connection. Every list item is a tuple (component, mount) where mount is a string describing whether the component is mounted at an edge or far from the edge.
    """
    
    subsystems = list()
    """
    List of all enabled subsystems.
    """
    
    couplings = list()
    """
    List of all couplings.
    """
    
    @property
    def impedance(self):
        """
        Total impedance at the coupling.
        """
        impedance = np.zeros(len(self.omega))
        for subsystem in self.subsystems:
            impedance = impedance + subsystem.impedance
        return impedance
    
    def get_coupling(self, subsystem_from, subsystem_to):
        """
        Return the coupling between subsystems for calculations.
        """
        return
    
    
    @property
    def routes(self):
        """
        Create a list.
        """
        return [(couplings.subsystem_from, coupling.subsystem_to) for coupling in couplings]
    
