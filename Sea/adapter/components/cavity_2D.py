"""
Adapter classes for :class:`Sea.model.components.ComponentCavity2D`
"""

import Sea
from .. import baseclasses


class SubsystemLong(baseclasses.SubsystemLong):
    model = Sea.model.components.cavity_2D.SubsystemLong()


class Component2DCavity(baseclasses.ComponentCavity):
    """
    3D cavity component.
    """
    
    name = "Cavity 2D"
    description = "A component describing a two-dimensional cavity."
    
    model = Sea.model.components.Component2DCavity()
    
    def __init__(self, obj, material, structure, position):
        baseclasses.ComponentCavity.__init__(self, obj, material, structure, position)
        obj.SubsystemLong = obj.makeSubsystem(SubsystemLong()) 