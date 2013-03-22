"""
Adapter classes for :class:`Sea.model.components.ComponentCavity3D`
"""

import Sea
from .. import baseclasses

class Component3DCavity(baseclasses.ComponentCavity):
    """
    3D cavity component.
    """
    
    name = "Cavity 3D"
    description = "A component describing a three-dimensional cavity."
    
    model = Sea.model.components.Component3DCavity()
    
    def __init__(self, obj, system, material, position):
        baseclasses.ComponentCavity.__init__(self, obj, system, material, position)
    