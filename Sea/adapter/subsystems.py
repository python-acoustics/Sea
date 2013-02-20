"""
The following are Subsystems classes encapsulating their respective Sea.model.subsystems class.
"""


import logging

import Sea
import baseclasses

class SubsystemLong(baseclasses.Subsystem):
    """
    A subsystem describing longitudinal waves in a structural component.
    """
    name = 'Longitudinal waves'
    description = 'A subsystem describing longitudinal waves in a structural component.'
    
    model = Sea.model.SubsystemLong()
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.Subsystem.__init__(self, obj, system, component, **properties)

class SubsystemBend(baseclasses.Subsystem):
    """
    A subsystem describing bending or flexural waves in a structural component.
    """
    name = 'Bending waves'
    description = 'A subsystem describing bending or flexural waves in a structural component.'
    model = Sea.model.SubsystemBend()
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.Subsystem.__init__(self, obj, system, component, **properties)
    

class SubsystemShear(baseclasses.Subsystem):
    """
    A subsystem describing shear waves in a structural component.
    """
    #model = Sea.model.SubsystemShear()
    
    name = 'Shear waves'
    description = 'A subsystem describing shear waves in a structural component.'
    def __init__(self, obj, system, component, **properties):
        baseclasses.Subsystem.__init__(self, obj, system, component, **properties)
    

class SubsystemCavity2D(baseclasses.Subsystem):
    """
    A subsystem describing a two-dimensional cavity.
    """
    name = 'Cavity 2D'
    description = 'A subsystem describing a two-dimensional cavity.'
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.Subsystem.__init__(self, obj, system, component, **properties)
    
class SubsystemCavity3D(baseclasses.Subsystem):
    """
    Subsystem for 3D cavities.
    """
    name = 'Cavity 3D'
    description = 'A subsystem describing a three-dimensional cavity.'
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.Subsystem.__init__(self, obj, system, component, **properties)    


import inspect, sys
subsystems_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
"""   