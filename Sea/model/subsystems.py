"""
Subsystems are the building blocks of an SEA model. Several types of subsystems have been defined.
"""  

import numpy as np
from baseclasses import SubsystemLong, SubsystemBend, SubsystemShear, SubsystemCavity

import abc



class SubsystemLongBeam(SubsystemLong):
    """
    Subsystem for longitudinal waves in a 1D system.
    """
    @property            
    def modal_density(self):
        """
        Modal density for longitudinal waves.
       
        .. math:: \\frac{N}{\\omega} = \\frac{L}{\pi c_L}
        """
        return np.repeat(self.component.length / (np.pi * self.soundspeed_group), len(self.omega))



class SubsystemBendBeam(SubsystemBend):
    """
    Subsystem for bending waves in a 1D system.
    """
   
    @property
    def modal_density(self):
        """
        Modal density for bending waves.
        """
        return self.component.length / (2.0 *np.pi *np.sqrt(self.omega))  * np.power((self.component.mass_per_area/self.component.bending_stiffness),(1/4))
        #return self.component.mass() / (4.0 * np.pi * np.sqrt(self.component.bending_stiffness() * self.component.mass_per_area()))
                


class SubsystemShearBeam(SubsystemShear):
    """
    Subsystem for shear waves in a 1D system.
    """
    pass
    

class SubsystemLongPlate(SubsystemLong):
    """
    Subsystem for longitudinal waves in a 2D system.
    """
    pass


class SubsystemBendPlate(SubsystemBend):
    """
    Subsystem for bending waves in a 2D system.
    """
    pass
    

class SubsystemShearPlate(SubsystemShear):
    """
    Subsystem for shear waves in a 2D system.
    """
    pass
    

class SubsystemCavity2D(SubsystemCavity):
    """
    Subsystem for a 2D room.
    """
    pass
    
class SubsystemCavity3D(SubsystemCavity):
    """
    Subsystem for a 3D room.
    """
    pass
    

