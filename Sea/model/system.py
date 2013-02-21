"""
The System class is the main class and contains methods for solving the SEA model.
"""

import math
import cmath
import numpy as np

import warnings
import weakref
import logging

from baseclasses import *
from components import *
from subsystems import *
from couplings import *
from excitations import *


class System(object):
    """
    The System class contains methods for solving the model.
    """
    
    
    # update lists through connector
    objects = list()
    components = list()
    subsystems = list()
    couplings = list()
    excitations = list()
    materials = list()
    parts = list()

    _frequency = np.array([1000, 2000, 4000, 8000])
    
     
    solved = False
    """
    Switch indicating whether the system (modal energies) were solved or not.
    """
    
    def _set_frequency(self, f):
        """
        Set frequency bands.
        
        :param f: is an iterable containing centerfrequencies
        """
        logging.info("SeaPy - System - _set_frequency - Setting frequency bands.")
        self._frequency = np.array(f) 
    
    def _get_frequency(self):
        """
        Get frequency bands.
        """
        return self._frequency
    
    frequency = property(fget=_get_frequency, fset=_set_frequency)     # Retrieve or set the frequency vector
    """
    This property is an array of centerfrequencies.
    """
    
    def _get_omega(self):
        return 2.0 * np.pi * self.frequency  
        
    omega = property(fget=_get_omega)
    """
    Angular frequency.
    
    .. math:: \\omega = 2 \\pi f
    
    """

    def createMatrix(self, subsystems, f):
        """
        Create loss factor matrix for given frequency band.
        
        :param subsystems: is a list of subsystems. Reason to give the list as argument instead of using self.subsystems is that that list might change during execution.
        :param f: is the index of the center frequency of the frequency band
        """
        logging.info('Creating matrix for centerfrequency %s', str(self.frequency[f]))
        
        print subsystems
        
        LF = np.zeros((len(subsystems), len(subsystems)), dtype=float)
        j = 0
        for subsystem_j in subsystems: # Row j 
            i = 0
            for subsystem_i in subsystems:       # Column i
                loss_factor = 0.0
                if i==j:
                    #print 'i = j'
                    ## Total loss factor: sum of damping loss factor + loss factors for power transported from i elsewhere
                    loss_factor = subsystem_i.component.material.loss_factor # Damping loss factor
                    for item in subsystem_i.linked_couplings_from: # + all CLFs 'from' i elsewhere
                        coupling = self.getObject(item)
                        loss_factor = loss_factor + coupling.clf[f] 
                
                else:
                    ####Take the coupling loss factor from subsystem i to subsystem j. Negative
                    x = list(set(subsystem_i.linked_couplings_from).intersection(set(subsystem_j.linked_couplings_to)))

                    ##if not x:
                    ## Use the relation consistency relationship?
                    ##pass
                    ##print 'error. No coupling?'
                    if len(x)==1:
                        coupling = x[0]
                        loss_factor = - self.getObject(coupling).clf()[f]
                    del x        
                LF[j,i] = loss_factor * subsystem_i.modal_density[f]
                i+=1
            j+=1
        logging.info('Matrix created.')
        
        logging.info(LF)
        return LF

    def clearResults(self):
        """
        Clear the results. Reset modal energies. Set :attr:`solved` to False.
        """
        logging.info('Clearing results...')
        
        for subsystem in self.subsystems:
            del subsystem.modal_energy
    
        self.solved = False
    
        logging.info('Cleared results.')
     
    def solveSystem(self):  # Put the actual solving in a separate thread
        """
        Solve energies for all subsystems.
        
        
        This method solves the modal energies for every subsystem.
        The method :meth:`createMatrix` is called for every frequency band to construct a matrix of :term:`loss factors` and :term:`modal densities`.
        
        """
        logging.info('Solving system...')
        

        subsystems = self.subsystems
        
        print subsystems
        
        f=0
        
        # Split this component. Create loss factor matrix and modal densities arrays seperately.
        for f in xrange(0, len(self.frequency), 1):
            LF = self.createMatrix(subsystems, f)
            
            # Create input power vector....we're still working for a single frequency now
            input_power = np.zeros(len(subsystems))
            modal_density = np.zeros(len(subsystems))

            
            i=0
            for subsystem in subsystems:
                modal_density[i] = subsystem.modal_density[f]
                input_power[i] = subsystem.input_power[f] / self.omega[f]   # Retrieve the power for the right frequency
                i=i+1
                

            #print input_power
            modal_energy = np.linalg.solve(LF, input_power)    # Left division results in the modal energies.
            #print E
            # Save each modal energy to its respective Subsystem nameect
            
            i = 0
            for subsystem in subsystems:
                subsystem.modal_energy[f] = modal_energy[i]
                i=i+1
            del modal_energy, input_power, LF
                
        self.solved = True  
        logging.info('System solved.')
    