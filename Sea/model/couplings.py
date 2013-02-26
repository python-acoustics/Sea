"""
Subsystems are connected to eachother through couplings.
"""


import numpy as np
from baseclasses import Coupling

"""All classes listed in this file are derived from the abstract SubSys class"""                


class CouplingJunction(Coupling):
    """Coupling of beams."""

    @property
    def tau(self, subsystem_from, subsystem_to):
        """
        Frequency averaged transmission coefficient
        
        ##.. math:: \\overline{\\tau_{12}} = \\frac{8 \\pi \\langle \\overline{G_1} \\rangle f \\eta_1 M_1}{1 + \\frac{\\eta_1}{\\eta_2}} \\frac{\\eta_2 + \\eta_{21}}{\\eta_12}
        
        .. math:: \\tau_{12} = \\frac{4 R_1 R_2}{\\left| \\sum_{i=1}^m Z_i \\right|^2}
        """
        return 4.0 * subsystem_from.resistance * subsystem_to.resistance / self.impedance**2.0
    
    @property
    def impedance(self):
        """
        Total impedance at the junction.
        """
        impedance = np.zeros(len(self.omega))
        for subsystem in self.subsystems:
            impedance = impedance + subsystem.impedance
        return impedance
        
        
    @property
    def clf(self, subsystem_from, subsystem_to):
        """Coupling loss factor."""
        #return self.tau() * self.subsystem_from.c_group() / (self.subsystem_from.omega * self.subsystem_from.component.length() * (2-self.tau()) )
        return np.real(subsystem_to.mobility()) / (2.0 * np.pi * self.omega * subsystem_from.component.mass + np.abs(self.subsystem_from.mobility() +   self.subsystem_to.mobility() )**2.0 )
             
###class CouplingLine(Coupling):
    ###"""Coupling of plate parts."""
    
    
    
    ###length = None
    
    ###@property
    ###def phi(self):
        ###"""Angle of incidence, vector."""
        ###return np.linspace(0, np.pi, self.phi_steps)

    ###@property
    ###def phi_step(self):
        ###"""Angle of incidence, stepsize."""
        ###return (np.pi - 0) / self.phi_steps
    
    ####def mu_B(self):
        ####return np.sqrt(k**2 +
    
    ###@property
    ###def power_inc(self):
        ###"""Incident power."""
        ###return self.subsystem_from.density * self.subsystem_from.velocity**2 * self.subsystem_from.soundspeed_group * self.subsystem_from.length / np.pi

    ###@property
    ###def power_trans(self):
        ###"""Power in plate j."""
        #### Depends on subsystem b type!
        #### Selection based on available classes!
        #### Bending wave
        ###if B:
            ###return self.subsys_b.density * self.subsys_b.omega**3 * alpha**2 / self.subsys_b.k() * np.sin(self.phi())
        #### Longitudinal wave
        ###elif L:
            ###return self.subsys_b.density * self.subsys_b.omega**3 * alpha**2 * self.subsys_b.k() * np.sin(self.phi()) / 2
        #### Shear wave
        ###elif S:
            ###return self.subsys_b.density * self.subsys_b.omega**3 * alpha**2 * self.subsys_b.k() * np.sin(self.phi()) / 2
        ###else:
            ###raise Exception('Subsystem does not exist.')
    
    ###@property
    ###def alpha(self):
            ###"""Alpha"""

    ###@property
    ###def tau_ij(self):
            ###"""Transmission coefficient as function of angular frequency and angle of incidence."""
            ###return self.power_trans()/self.power_inc()
    
    ###@property
    ###def tau(self):
            ###"""Transmission coefficient as function of angular frequency. Integration/summation is done over all the angles."""
            ####return 0.5 * np.sum(self.tau_ij() * np.sin(self.phi) * self.phi_step()      # Dimensions! Inner product. Needs to duplicate along omega 
    
    ###@property
    ###def clf(self):
            ###"""Coupling loss factor"""
            ###return self.tau * self.subsystem_from.soundspeed_group * self.length / (self.omega * np.pi * self.S)

###class CouplingSurface(Coupling):
    ###"""Coupling of 3D components."""


    
    ###reduction_index = None
    ###"""
    ###Sound reduction index
    ###"""
    
    ###@property
    ###def tau(self):
        ###return 10**(-self.reduction_index/10)
    ###"""
    ###Transmission coefficient
    ###"""
    
    ###surface = None
    ###"""
    ###Surface of the coupling
    ###"""
    
    ###@property
    ###def clf(self):
        ###"""
        ###Coupling loss factor.
        ###"""
        ###return self.subsystem_to.soundspeed_phase * self.surface/ (4.0 * self.omega * self.subsystem_to.component.volume) * self.tau 
        
    


