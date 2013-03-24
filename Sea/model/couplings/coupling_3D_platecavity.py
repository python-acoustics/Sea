import numpy as np
from ..baseclasses import Coupling


class Coupling3DPlateCavity(Coupling):
    
    
    @property
    def impedance_from(self):
        return self.subsystem_from.impedance
    
    @property
    def impedance_to(self):
        return self.subsystem_to.impedance
    
    @property
    def critical_frequency(self):
        """
        Critical frequency.
        
        .. math:: f_c = \\frac{ c_0^2  } {1.8 c_L t}
        
        See BAC, 3.2.2 script.
        """
        return self.subsystem_to.soundspeed_group**2.0 / (1.8 * self.subsystem_from.soundspeed_group * self.component_from.thickness)
    
    @property
    def critical_wavelength(self):
        """
        Wavelength belonging to critical frequency.
        """
        return self.soundspeed_group / self.critical_frequency
        
    @property
    def radiation_efficiency(self):
        """
        Radiation efficiency of a plate for bending waves.
        
        See TA2 Radiation plateapp_ta2
        """      
        
        f = np.array(self.frequency, dtype=complex)
        """Cast to complex numbers to prevent errors with sqrt further down."""
        
        fc = self.critical_frequency
        lc = self.critical_wavelength
        
        Lx = self.component.length
        Ly = self.component.width
        S = self.component.area
        U = 2.0 * (self.length + self.width)
        
        fc_band = (fc > self.lower) * (fc < self.upper)
        f_lower = fc > self.upper
        f_upper = fc < self.lower
        
        alpha = np.sqrt(f/fc)
        g1 =  ( 4.0 / np.pi**4.0 * (1.0 - 2.0 * alpha**2.0) / np.sqrt(1.0 - alpha**2.0) ) * (f < 0.5 * fc)
        g2 = 1.0 / (4.0 * np.pi**4.0) * (  (1.0 - alpha**2) * np.log((1.0+alpha)/(1.0-alpha)) + 2.0 * alpha ) / (1.0-alpha**2.0)**1.5
        sigma1 = lc**2.0 / S * (2.0 * g1 + U / lc * g2)
        sigma2 = np.sqrt(Lx/lc) + np.sqrt(Ly/lc)
        sigma3 = (1.0 - fc/f)**(-0.5)
        
        sigma1 = np.nan_to_num(sigma1)
        sigma2 = np.nan_to_num(sigma2)
        sigma3 = np.nan_to_num(sigma3)
        """Replace NaN with zeros"""
        
        sigma = sigma1 * f_lower + sigma2 * fc_band  + sigma3 * f_upper * (sigma3 < sigma2)
        sigma = np.real(np.nan_to_num(sigma))
        return sigma
    
    
    
    
    @property
    def clf(self):
        """
        Coupling loss factor for plate to cavity radiation.
        
        .. math:: \\eta_{plate, cavity} = \\frac{\\rho_0 c_0 \\sigma}{\\omega m^{''}}
        
        .. attention::
            Which speed of sound???
        
        See BAC, equation 3.6
        """
        try:
            return self.subsystem_from.component.material.density * self.subsystem_to.soundspeed_group * \
                   self.subsystem_from.radiation_efficiency / (self.omega * self.subsystem_from.component.mass_per_area)
        except ZeroDivisionError:
            return np.zeros(len(self.frequency))