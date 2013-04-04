"""
Adapter class for :class:`Sea.model.components.Component1DBeam`
"""

import Sea
from .. import baseclasses

class SubsystemLong(baseclasses.SubsystemLong):
    model = Sea.model.components.structural_1D_beam.SubsystemLong()

class SubsystemBend(baseclasses.SubsystemBend):
    model = Sea.model.components.structural_1D_beam.SubsystemBend()

class SubsystemShear(baseclasses.SubsystemShear):
    model = Sea.model.components.structural_1D_beam.SubsystemShear()


class Component1DBeam(baseclasses.ComponentStructural):
    """
    Beam structural component.
    
    This adapter describes a :class:`Sea.model.components.Component1DBeam`
    """
    name = 'Beam'
    description = 'A structural component with wave propagation along one dimension.'
    
    model = Sea.model.components.Component1DBeam()
    
    def __init__(self, obj, material, part):
        baseclasses.ComponentStructural.__init__(self, obj, material, part)
        
        obj.addProperty("App::PropertyLength", "Length", "Beam", "Length of the beam")
        obj.setEditorMode("MaxLength", 2)
        
        obj.addProperty("App::PropertyFloat", "CrossSection", "Beam", "Cross section of the beam")
        obj.setEditorMode("CrossSection", 2)
        
        obj.addProperty("App::PropertyFloat", "MassPerArea", "Beam", "Mass per unit area")
        obj.addProperty("App::PropertyFloat", "AreaMoment", "Beam", "Area moment of inertia")

        obj.SubsystemLong = obj.makeSubsystem(SubsystemLong())
        obj.SubsystemBend = obj.makeSubsystem(SubsystemBend()) 
        obj.SubsystemShear = obj.makeSubsystem(SubsystemShear()) 

    def onChanged(self, obj, prop):
        baseclasses.ComponentStructural.onChanged(self, obj, prop)
        
        if prop == 'Length':
            obj.Proxy.model.length = obj.Length
    
    def execute(self, obj):
        baseclasses.ComponentStructural.execute(self, obj)
        
        obj.Length = obj.Proxy.model.length
        obj.AreaMoment = obj.Proxy.model.area_moment_of_inertia
        obj.CrossSection = obj.Proxy.model.cross_section
        
    
 
   
        
    