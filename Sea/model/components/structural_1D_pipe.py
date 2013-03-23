import numpy as np
from ..baseclasses import ComponentStructural, SubsystemStructural




class SubsystemLong(SubsystemStructural):
    pass


class SubsystemBend(SubsystemStructural):
    pass

class SubsystemShear(SubsystemStructural):
    pass



















    
class ComponentPipe(ComponentStructural):
    """
    One-dimensional beam component.
    """
    pass
    
    
    #def __init__(self):
        #"""
        #Constructor
        #"""
        #self.subsystem_long = SubsystemLong(self)
        #"""
        #Subsystem describing longitudinal waves.
        #"""
        #self.subsystem_bend = SubsystemBend(self)
        #"""
        #Subsystem describing bending waves.
        #"""
        #self.subsystem_shear = SubsystemShear(self)
        #"""
        #Subsystem describing shear waves.
        #"""
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by :math:`\\sqrt{2}`.
        See Lyon, above eq. 8.1.10
        .. math:: \\kappa = \\frac{h}{\\sqrt{2}}
        """
        return self.height / 12