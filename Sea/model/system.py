"""
The System class is the main class and contains methods for solving the SEA model.
"""

import math
import cmath
import numpy as np

import warnings
import weakref
import logging


class System(object):
    """
    The System class contains methods for solving the model.
    """
    
    
    # update lists through connector
    #objects = list()
    #components = list()
    subsystems = list()
    couplings = list()
    excitations = list()
    #materials = list()
    #parts = list()

    _frequency = np.array([1000, 2000, 4000, 8000])
    
     
    solved = False
    """
    Switch indicating whether the system (modal energies) were solved or not.
    """
    
    _octave_true = np.array([
        0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 
        0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
    """
    Which frequency bands should be used when calculating in 1/1-octave bands.
    """
    _third_true = np.array([
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    """
    Which frequency bands should be used when calculating in 1/3-octave bands.
    """
    
    """
    Centerfrequencies of 1/3-octave bands.
     
    """

    frequency = np.array([
        25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 
        400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 
        4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
    """
    Frequency is an array of centerfrequencies.
    """
 
    
    octaves = False
    """
    Switch to indicate whether 1/1-octaves (True) are used or 1/3-octaves (False).
    """
    
    
    def _set_enabled_bands(self, x):
        if len(x) == len(self.frequency):
            if self.octaves:
                self._enabled_bands = np.array(x * self._octave_true) 
            else:
                self._enabled_bands = np.array(x)
                
    
    def _get_enabled_bands(self):
        return self._enabled_bands

    _enabled_bands = np.ones(len(frequency))
    enabled_bands = property(fget=_get_enabled_bands, fset=_set_enabled_bands)
    """"
    Specify with booleans which :attr:`frequency` are used. 
    Checks on assignment whether 1/1-octaves should be used or 1/3-octaves.
    """
    

    
    @property
    def omega(self):
        """
        Angular frequency.
        
        .. math:: \\omega = 2 \\pi f
        
        """
        return 2.0 * np.pi * self.frequency  


    def createMatrix(self, subsystems, f):
        """
        Create loss factor matrix for given frequency band.
        
        :param subsystems: is a list of subsystems. Reason to give the list as argument instead of using self.subsystems is that that list might change during execution.
        :param f: is the index of the center frequency of the frequency band
        """
        logging.info('Creating matrix for centerfrequency %s', str(self.frequency[f]))
        
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
                    for coupling in subsystem_i.linked_couplings_from: # + all CLFs 'from' i elsewhere
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
                        loss_factor = - coupling.clf[f]
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
        """Solve modal powers.
        
        This method solves the modal energies for every subsystem.
        The method :meth:`createMatrix` is called for every frequency band to construct a matrix of :term:`loss factors` and :term:`modal densities`.
        
        """
        logging.info('Solving system...')
        

        subsystems = self.subsystems
        
       
        for f in xrange(0, len(self.frequency), 1): # For every frequency band
            if self.enabled_bands[f]:               # If it is enabled
                LF = self.createMatrix(subsystems, f)   # Create a loss factor matrix.
                
                input_power = np.zeros(len(subsystems))     # Create input power vector
                
                i=0
                for subsystem in subsystems:
                    input_power[i] = subsystem.input_power[f] / self.omega[f]   # Retrieve the power for the right frequency
                    i=i+1
                    
                try:
                    modal_energy = np.linalg.solve(LF, input_power)    # Left division results in the modal energies.
                except np.linalg.linalg.LinAlgError as e:   # If there is an error solving the matrix, then quit right away.
                    warnings.warn( repr(e) )
                    return
                # Save each modal energy to its respective Subsystem nameect
                
                i = 0
                for subsystem in subsystems:
                    subsystem.modal_energy[f] = modal_energy[i]
                    i=i+1
                del modal_energy, input_power, LF
                
        self.solved = True  
        logging.info('System solved.')
    