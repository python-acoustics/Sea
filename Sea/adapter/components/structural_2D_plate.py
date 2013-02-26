"""
Adapter classes for :class:`Sea.model.components.Component2DPlate`
"""

import Sea
from .. import baseclasses

class Component2DPlate(baseclasses.Component):
    """
    Plate structural component.
    """

    name = 'Plate'
    description = 'A structural component with wave propagation along two dimensions.'
    
    model = Sea.model.components.Component2DPlate()  
    """
    This adapter describes a :class:`Sea.model.components.ComponentPlate`
    """
    
    def __init__(self, obj, system, material, part, **properties):
        baseclasses.ComponentStructural.__init__(self, obj, system, material, part, **properties)
        
        obj.addProperty("App::PropertyFloat", "Thickness", "Thickness of the plate")
        
    def onChanged(self, obj, prop):
        baseclasses.ComponentStructural.onChanged(self, obj, prop)
    
    def execute(self, obj):
        baseclasses.ComponentStructural.execute(self, obj)
        
        obj.Thickness = self.model.thickness
