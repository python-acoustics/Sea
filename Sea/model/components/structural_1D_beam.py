"""
Classes describing a one-dimensional beam.
"""

import numpy as np
from ..baseclasses import ComponentStructural, SubsystemStructural

   
class SubsystemLong(SubsystemStructural):
    """
    Subsystem for longitudinal waves in a 1D system.
    """
    
    @property
    def wavenumber(self, N, delta):
        """
        Wavenumber in radians per unit length.
        
        :param N: mode
        :param delta: boundary condition dependent constant
        
        .. math:: k = (N + \\delta_{BC} ) \\frac{\\pi}{L}
        
        See Lyon, equation 8.1.2
        """
        return (N + delta) * np.pi / self.component.length
    
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for longitudinal wave.
        
        .. math:: c_{L,\\phi}^{1D} = \\frac{E}{\\rho}
        """
        return np.repeat(self.component.material.young / self.component.material.density, len(self.omega))

    @property
    def soundspeed_group(self):
        """
        Group velocity for longitudinal wave.
        
        .. math:: c_{L,g}^{1D} = c_{L,\\phi}^{1D}
        """
        return self.soundspeed_phase
    
    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for longitudinal waves.
        
        .. math:: \\overline{\\delta f}_L^{1D} = \\frac{c_{L, \\phi}^{1D}}{2L}
        
        See Lyon, eq. 8.1.7
        """
        return self.soundspeed_group / (2.0 * self.component.length)
        
    @property
    def impedance_force_point_edge(self):
        """
        Impedance for longitudinal waves in a bar when excited at a point by a force.
    
        .. math:: Z_{L}^{F, 1D} = 2 \\rho S c_L
        
        See Lyon, table 10.1, first row.
        """
        return 2.0 * self.component.material.density * self.component.cross_section * self.soundspeed_group
    
   
class SubsystemBend(SubsystemStructural):
    """
    Subsystem for bending waves in a 1D system.
    """
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for bending wave.
        
        .. math:: c_{B,\\phi}^{2D} = \\sqrt{\\omega \\kappa c_{L, \\phi}^{1D} }
        
        See Lyon, above eq. 8.1.10
        """
        return np.sqrt(self.omega * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_phase)
                
    @property
    def soundspeed_group(self):
        """
        Group velocity for bending wave.
        
        .. math:: c_{B,g}^{1D} = 2 c_{B,\\phi}^{1D}
        
        """
        return 2.0 * self.soundspeed_phase
        
    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for bending waves. Valid when :math:`f << c_{L,\\phi}  / 4 \\pi \\kappa`.
        
        .. math:: \\overline{\\delta f}_B^{1D} = \\frac{c_{B, \\phi}^{1D}}{L}
        
        See Lyon, eq. 8.1.10
        """
        return self.soundspeed_group / (self.component.length)

    @property
    def impedance_force_point_center(self):
        """
        Impedance for bending waves in a thin beam excited far way from the edges.
        
        .. math:: Z_B^{F,1D} = 2 \\rho S c_{L, \\phi}^{1D} (1 + j)
        
        See Lyon, table 10.1, second row.
        """
        return 2.0 * self.component.material.density * self.component.cross_section * self.soundspeed_group * (1.0 + 1.0j)

    @property
    def impedance_force_point_edge(self):
        """
        Impedance for bending waves in a thin beam excited on the side.
        
        .. math:: Z_B^{F,1D} = \\frac{1}{2} \\rho S c_{L, \\phi}^{1D} (1 + j)
        
        See Hynna, table 1, second equation.
        """
        return 0.5 * self.component.material.density * self.component.cross_section * self.soundspeed_group * (1.0 + 1.0j)

    
    @property
    def impedance_moment_center(self):
        """
        Moment impedance for bending waves excited in the center of the beam.
        
        .. math:: W = 2 \\rho S c_B \\frac{(1-j)}{k_B^2}
        
        See Hynna, table 1.
        """
        return 2.0 * self.component.material.density * self.component.cross_section * self.soundspeed_group * (1.0 - 1.0j) / self.wavenumber**2.0
        
    
    @property
    def impedance_moment_edge(self):
        """
        Moment impedance for bending waves excited at the edge of the beam.
        
        .. math:: W = \\frac{1}{2} \\rho S c_B \\frac{(1-j)}{k_B^2} 
        
        See Hynna, table 1.
        """
        return 0.5 * self.component.material.density * self.component.cross_section * self.soundspeed_group * (1.0 - 1.0j) / self.wavenumber**2.0
    
    
class SubsystemShear(SubsystemStructural):
    """
    Subsystem for shear waves in a 1D isotropic system.
    """
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for shear wave.
        
        .. math:: c_{T,g}^{1D} = \\sqrt{\\frac{G J }{\\rho I_p}}
        """
        return np.sqrt(self.component.material.shear * self.component.torsional_rigidity / (self.component.material.density * self.component.area_moment_of_inertia))

    @property
    def soundspeed_group(self):
        """
        Group velocity for shear wave.
        
        .. math:: c_{T,g}^{1D} = c_{T,\\phi}^{1D}
        
        """
        return self.soundspeed_phase

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for bending waves.
        
        .. math:: \\overline{\\delta f}_T^{1D} = \\frac{c_T}{2L}
        
        See Lyon, eq. 8.1.8
        """
        return self.soundspeed_group / (2.0 * self.component.length)
        
        
    @property
    def impedance(self):
        return 0.0
        
class Component1DBeam(ComponentStructural):
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
    
    
    
    def __init__(self):
        """
        Constructor
        """
        self.subsystem_long = SubsystemLong(self)
        """
        An instance of :class:`SubsystemLong` describing longitudinal waves.
        """
        self.subsystem_bend = SubsystemBend(self)
        """
        An instance of :class:`SubsystemBend` describing bending waves.
        """
        self.subsystem_shear = SubsystemShear(self)
        """
        an instance of :class:`SubsystemShear` describing shear waves.
        """
    
    @property
    def mass_per_area(self):
        """
        Mass per unit area.
        """
        return self.material.density * self.height #*self.width
             
    @property
    def area_moment_of_inertia(self):
        """
        Area moment of inertia.
        """
        return np.sqrt(self.cross_section) * np.power(np.sqrt(self.cross_section),3.0) / 12.0
            
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by 12.
        
        .. math:: \\kappa = \\frac{h}{12}
        
        See Lyon, above eq. 8.1.10
        """
        return self.height / 12.0
    


        