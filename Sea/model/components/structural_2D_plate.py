"""
Classes describing a two-dimensional plate.
"""

import numpy as np
from ..baseclasses import ComponentStructural, SubsystemStructural


class SubsystemLong(SubsystemStructural):
    """
    Subsystem for longitudinal waves in a 2D isotropic component.
    """
    
    @property
    def soundspeed_group(self):
        """
        Group velocity for longitudinal waves in a 2D isotopic plate.
        
        .. math:: c_L^{'} = \\sqrt{\\frac{E}{\\rho \\left( 1 - \\mu^2 \\right)}}
        
        See Lyon, above eq 8.2.5 
        """
        return np.sqrt(self.component.material.young / (self.component.material.density * (1.0 - self.component.material.poisson**2.0)))
    
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for longitudinal waves in a 2D isotropic plate.
        
        .. math:: c_{group} = c_{phase} = c_L
        
        See Lyon, above eq 8.2.8
        """
        return self.soundspeed_group
    
    @property
    def average_frequency_spacing(self):
        """"
        Average frequency spacing for a 2D isotropic plate.
        
        .. math:: \\overline{\delta f}_S^{2D} = \\frac{{c_L^1}^2}{\\omega A}
        """
        return  self.soundspeed_group**2.0 / (self.omega * self.A)


        
        
class SubsystemBend(SubsystemStructural):
    """
    Subsystem for bending waves in a 2D isotropic component.
    """

    @property
    def soundspeed_phase(self):
        """
        Phase velocity for bending wave.
        
        .. math:: c_{B,\\phi}^{2D} = \\sqrt{\\omega \\kappa c_L^{'}}
        
        See Lyon, above eq. 8.2.5
        """
        return np.sqrt(self.omega * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_phase)
                
    @property
    def soundspeed_group(self):
        """
        Group velocity for bending wave.
        
        .. math:: c_{B, g}^{2D} = 2 c_{B,\\phi}^{2D}
        
        See Lyon, above eq. 8.2.5
        """
        return 2.0 * self.soundspeed_phase
    
    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for bending waves in a 2D isotropic plate.
        
        .. math:: \\overline{\\delta f}_B^{2D} = \\frac{2 \\kappa c_L^{', 2D}}{A}
        
        See Lyon, eq 8.2.5
        """
        return 2.0 * self.component.radius_of_gyration * self.soundspeed_group_long / self.component.area
    
class SubsystemShear(SubsystemStructural):
    """
    Subsystem for shear waves in a 2D isotopic component.
    """
    
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for shear waves in a 2D isotropic plate.
        
        .. math:: c_S = \\sqrt{\\frac{G}{\\rho}}
        
        See Lyon, above eq. 8.2.5
        """
        return np.sqrt(self.component.material.shear_modulus / self.component.material.density)
                
    @property
    def soundspeed_group(self):
        """
        Group velocity for shear wavees in a 2D isotropic plate.
        
        .. math:: c_{group} = c_{phase} = 2 C_S
        
        See Lyon, above eq. 8.2.5
        """
        return self.soundspeed_phase

    @property
    def average_frequency_spacing(self):
        """"
        Average frequency spacing for shear waves in a 2D isotropic plate.
        
        .. math:: \\overline{\\delta f}_S^{2D} = \\frac{c_S^2}{\\omega A}
        
        See Lyon, eq 8.2.5
        """
        return self.soundspeed_group**2.0 / (self.omega * self.component.area)
   
   
class Component2DPlate(ComponentStructural):
    """
    Two-dimensional plate component.
    """

    thickness = None
    """
    Thickness of the plate.
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.subsystem_long = SubsystemLong(self)
        """
        Subsystem describing longitudinal waves.
        """
        self.subsystem_bend = SubsystemBend(self)
        """
        Subsystem describing bending waves.
        """
        self.subsystem_shear = SubsystemShear(self)
        """
        Subsystem describing shear waves.
        """
        
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the plate by :math:`\\sqrt{12}`.
        
        .. math:: \\kappa = \\frac{h}{\\sqrt{12}}
        
        See Lyon, above eq. 8.2.5
        """
        return self.height / np.sqrt(12.0)
        
        
    @property
    def area_moment_of_inertia(self):
        """
        Area moment of inertia.
        
        .. math:: J = \\frac{t^3}{12 \\left( 1 - \\nu^2 \\right)}
        """
        return self.thickness**3.0 / (12.0 * (1.0 - self.poisson()**2.0))
 


   