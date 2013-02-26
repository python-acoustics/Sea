"""
Adapter classes for :class:`Sea.model.components.ComponentCavity2D`
"""

class SubsystemCavity2D(baseclasses.SubsystemCavity):
    """
    A subsystem describing a two-dimensional cavity.
    """
    name = 'Cavity 2D'
    description = 'A subsystem describing a two-dimensional cavity.'
    
    model = Sea.model.SubsystemCavity2D
    
    def __init__(self, obj, system, component, **properties):
        baseclasses.SubsystemCavity.__init__(self, obj, system, component, **properties)
    