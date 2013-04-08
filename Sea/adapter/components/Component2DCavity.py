"""
Adapter classes for :class:`Sea.model.components.ComponentCavity2D`
"""

import Sea
from ..subsystems import SubsystemLong
from ComponentCavity import ComponentCavity

class SubsystemLong(SubsystemLong, Sea.model.components.Component2DCavity.SubsystemLong):
    pass


class Component2DCavity(ComponentCavity, Sea.model.components.Component2DCavity.Component2DCavity):
    """
    3D cavity component.
    """
    
    name = "Cavity 2D"
    description = "A component describing a two-dimensional cavity."
    
    def __init__(self, obj, material, structure, position):
        ComponentCavity.__init__(self, obj, material, structure, position)
        obj.SubsystemLong = obj.makeSubsystem(SubsystemLong()) 