"""
Adapter class for :class:`Sea.model.components.Component1DBeam`
"""

import Sea
from ComponentStructural import ComponentStructural
from ..subsystems import SubsystemLong, SubsystemBend, SubsystemShear

class SubsystemLong(SubsystemLong, Sea.model.components.Component1DBeam.SubsystemLong):
    pass

class SubsystemBend(SubsystemBend, Sea.model.components.Component1DBeam.SubsystemBend):
    pass

class SubsystemShear(SubsystemShear, Sea.model.components.Component1DBeam.SubsystemShear):
    pass


class Component1DBeam(ComponentStructural, Sea.model.components.Component1DBeam.Component1DBeam):
    """
    Beam structural component.
    
    This adapter describes a :class:`Sea.model.components.Component1DBeam`
    """
    name = 'Beam'
    description = 'A structural component with wave propagation along one dimension.'
    
    
    def __init__(self, obj, material, part):
        ComponentStructural.__init__(self, obj, material, part)
        
        obj.addProperty("App::PropertyLength", "Length", "Beam", "Length of the beam")
        obj.setEditorMode("MaxLength", 1)
        
        obj.addProperty("App::PropertyFloat", "CrossSection", "Beam", "Cross section of the beam")
        obj.setEditorMode("CrossSection", 1)
        
        obj.addProperty("App::PropertyFloat", "MassPerArea", "Beam", "Mass per unit area")
        obj.setEditorMode("MassPerArea", 1)
        obj.addProperty("App::PropertyFloat", "AreaMoment", "Beam", "Area moment of inertia")
        obj.setEditorMode("AreaMoment", 1)
        
        self.SubsystemLong = obj.makeSubsystem(SubsystemLong())
        self.SubsystemBend = obj.makeSubsystem(SubsystemBend()) 
        self.SubsystemShear = obj.makeSubsystem(SubsystemShear()) 

    def onChanged(self, obj, prop):
        ComponentStructural.onChanged(self, obj, prop)
        
        if prop == 'Length':
            obj.Proxy.model.length = obj.Length
    
    def execute(self, obj):
        ComponentStructural.execute(self, obj)
        
        obj.Length = obj.Proxy.model.length
        obj.AreaMoment = obj.Proxy.model.area_moment_of_inertia
        obj.CrossSection = obj.Proxy.model.cross_section
        
    
 