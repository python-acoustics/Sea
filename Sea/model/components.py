"""
Component classes describe structural components and cavities.
"""

import numpy as np
from baseclasses import Component

   
class ComponentBeam(Component):
    """
    One-dimensional beam component.
    """


    length = 0.0
    """
    Length of the beam
    """
    
    cross_section = 0.0
    """
    Cross section of the beam
    """
    
    height = 0.0
    """
    Height of the beam
    """
    
    @property
    def mass_per_area(self):
        """Mass per unit area."""
        return self.material.density * self.height #*self.width
             
    @property
    def area_moment_of_inertia(self):
        """Area moment of inertia."""
        return np.sqrt(self.cross_section) * np.power(np.sqrt(self.cross_section),3.0) / 12.0
             
    @property
    def mobility_long(self):
        """Mobility for longitudinal waves :math:`Y_{long}`."""
        return 1.0 / (2.0 * self.cross_section * np.sqrt(self.material.young * self.material.density))
        
    @property
    def mobility_bend(self):
        """Mobility for flexural waves :math:`Y_{bend}`."""
        return (1.0 - 1j) / (4.0 * self.cross_section * self.material.density * np.sqrt(self.omega)) * np.power(self.cross_section * self.material.density / (self.material.young * self.area_moment_of_inertia()), 0.25)
            
    @property
    def mobility_shear(self):
        """Mobility for shear waves :math:`Y_{shear}`."""
        return 
    
class ComponentPlate(Component):
    """
    Two-dimensional plate component.
    """
    

    thickness = None
    """
    Thickness of the plate.
    """
    
    @property
    def area_moment_of_inertia(self):
        """
        Area moment of inertia.
        
        .. math:: J = \\frac{t^3}{12 \\left( 1 - \\nu^2 \\right)}
        """
        return self.thickness**3 / (12.0 * (1.0 - self.poisson()**2))
                
class Cavity(Component):
    """
    Cavity or room component.
    """
    
    __name__ = 'Cavity'
    name = 'Cavity'
    description = 'A cavity is a non-structural volume.'
    
    
    pass
                
components_map = {
    'beam' : ComponentBeam,
    'plate' : ComponentPlate,
}


