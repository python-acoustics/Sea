"""
The following are Subsystems classes encapsulating their respective :mod:`Sea.model.subsystems` class.
"""


import logging

import Sea
import baseclasses

class SubsystemLongBeam(baseclasses.SubsystemLong):
    """
    A subsystem describing longitudinal waves in a structural 1D component.
    """
    name = 'Longitudinal waves'
    description = 'A subsystem describing longitudinal waves in a structural 1D component.'
    
    model = Sea.model.SubsystemLongBeam()
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemLong.__init__(self, obj, system, component, **properties)

class SubsystemBendBeam(baseclasses.SubsystemBend):
    """
    A subsystem describing bending or flexural waves in a structural 1D component.
    """
    name = 'Bending waves'
    description = 'A subsystem describing bending or flexural waves in a structural 1D component.'
    model = Sea.model.SubsystemBendBeam()
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemBend.__init__(self, obj, system, component, **properties)
    

class SubsystemShearBeam(baseclasses.SubsystemShear):
    """
    A subsystem describing shear waves in a structural 1D component.
    """
    #model = Sea.model.SubsystemShearBeam()
    
    name = 'Shear waves'
    description = 'A subsystem describing shear waves in a structural 1D component.'
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemShear.__init__(self, obj, system, component, **properties)
    

class SubsystemCavity2D(baseclasses.SubsystemCavity):
    """
    A subsystem describing a two-dimensional cavity.
    """
    name = 'Cavity 2D'
    description = 'A subsystem describing a two-dimensional cavity.'
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemCavity.__init__(self, obj, system, component, **properties)
    
class SubsystemCavity3D(baseclasses.SubsystemCavity):
    """
    Subsystem for 3D cavities.
    """
    name = 'Cavity 3D'
    description = 'A subsystem describing a three-dimensional cavity.'
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemCavity.__init__(self, obj, system, component, **properties)    


import inspect, sys
subsystems_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
"""   