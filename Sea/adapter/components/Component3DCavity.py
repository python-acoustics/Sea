"""
Adapter classes for :class:`Sea.model.components.ComponentCavity3D`
"""

import Sea
from ..subsystems import SubsystemCavityLong
from ComponentCavity import ComponentCavity

class SubsystemLong(SubsystemCavityLong, Sea.model.components.Component3DCavity.SubsystemLong):
    """Subsystem for longitudinal waves in a 3D cavity.
    """
    pass


class Component3DCavity(ComponentCavity, Sea.model.components.Component3DCavity.Component3DCavity):
    """
    3D cavity component.
    """
    
    name = "Cavity 3D"
    description = "A component describing a three-dimensional cavity."
    
    
    def __init__(self, obj, system, material, position):
        ComponentCavity.__init__(self, obj, system, material, position)
        self.SubsystemLong = obj.makeSubsystem(SubsystemLong)
    