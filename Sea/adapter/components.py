"""
The following are Component classes encapsulating their respective Sea.model.components. class.
"""

import logging

import Sea
import baseclasses

class ComponentBeam(baseclasses.Component):
    """
    Beam structural component.
    """
    name = 'Beam'
    description = 'A structural component with wave propagation along one dimension.'

    model = Sea.model.ComponentBeam()
    
    def __init__(self, obj, system, material, part, **properties):
        baseclasses.Component.__init__(self, obj, system, material, part, **properties)
        
        obj.addProperty("App::PropertyLength", "Length", "Beam", "Length of the beam")
        obj.setEditorMode("MaxLength", 2)
        
        obj.addProperty("App::PropertyFloat", "CrossSection", "Beam", "Cross section of the beam")
        obj.setEditorMode("CrossSection", 2)
        
        obj.addProperty("App::PropertyFloat", "MassPerArea", "Beam", "Mass per unit area")
        obj.addProperty("App::PropertyFloat", "AreaMoment", "Beam", "Area moment of inertia")


    def onChanged(self, obj, prop):
        baseclasses.Component.onChanged(self, obj, prop)
        
        if prop == 'Length':
            self.model.length = obj.Length
    
    def execute(self, obj):
        baseclasses.Component.execute(self, obj)
        
        obj.Length = self.model.length
        obj.AreaMoment = self.model.area_moment_of_inertia
        obj.CrossSection = self.model.cross_section
        
            
class ComponentPlate(baseclasses.Component):
    """
    Plate structural component.
    """

    name = 'Plate'
    description = 'A structural component with wave propagation along two dimensions.'
    
    model = Sea.model.ComponentPlate()  
    
    def __init__(self, obj, system, material, part, **properties):
        baseclasses.Component.__init__(self, obj, system, material, part, **properties)
        
        obj.addProperty("App::PropertyFloat", "Thickness", "Thickness of the plate")
        
    def execute(self, obj):
        baseclasses.Component.execute(self, obj)
        
        obj.Thickness = self.model.thickness

        
        
import inspect, sys
components_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available components.
"""