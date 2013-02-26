"""
Adapter classes for :class:`Sea.model.components.ComponentCavity3D`
"""

class SubsystemCavity3D(baseclasses.SubsystemCavity):
    """
    A subsystem describing a three-dimensional cavity.
    """
    name = 'Cavity 3D'
    description = 'A subsystem describing a three-dimensional cavity.'
    
    model = Sea.model.SubsystemCavity2D
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemCavity.__init__(self, obj, system, component, **properties)    
