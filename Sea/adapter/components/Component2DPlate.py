"""
Adapter classes for :class:`Sea.model.components.Component2DPlate`
"""

import Sea
from ComponentStructural import ComponentStructural
from ..subsystems import SubsystemLong, SubsystemBend, SubsystemShear

class SubsystemLong(SubsystemLong, Sea.model.components.Component2DPlate.SubsystemLong):
    """Subsystem for longitudinal waves in a plate.
    """
    pass

class SubsystemBend(SubsystemBend, Sea.model.components.Component2DPlate.SubsystemBend):
    """Subsystem for bending waves in a plate.
    """
    pass

class SubsystemShear(SubsystemShear, Sea.model.components.Component2DPlate.SubsystemShear):
    """Subsysem for shear waves in a plate.
    """
    pass

    
class Component2DPlate(ComponentStructural, Sea.model.components.Component2DPlate.Component2DPlate):
    """Plate structural component.
    
    This adapter describes a :class:`Sea.model.components.Component2DPlate`
    """

    name = 'Plate'
    description = 'A structural component with wave propagation along two dimensions.'
    
    def __init__(self, obj, system, material, part):
        
        obj.addProperty("App::PropertyFloat", "Length", self.name, "Length of the plate.")
        obj.setEditorMode("Length", 1)
        obj.addProperty("App::PropertyFloat", "Width", self.name, "Width of the plate.")
        obj.setEditorMode("Width", 1)
        ComponentStructural.__init__(self, obj, system, material, part)
        
        
        obj.addProperty("App::PropertyFloat", "Area", self.name, "Area of the plate.")
        obj.setEditorMode("Area", 1)
        obj.addProperty("App::PropertyFloat", "Thickness", self.name, "Thickness of the plate.")
        obj.setEditorMode("Thickness", 1)
        obj.addProperty("App::PropertyFloat", "MassPerArea", self.name, "Mass per unit area.")
        obj.setEditorMode("MassPerArea", 1)
        self.calc_area_and_thickness(obj)
        
        
        self.SubsystemLong = obj.makeSubsystem(SubsystemLong)
        self.SubsystemBend = obj.makeSubsystem(SubsystemBend) 
        self.SubsystemShear = obj.makeSubsystem(SubsystemShear) 

        
    def onChanged(self, obj, prop):
        ComponentStructural.onChanged(self, obj, prop)
        
        if prop == 'Area':
            obj.Proxy.area = obj.Area
        
        elif prop == 'Thickness':
            obj.Proxy.thickness = obj.Thickness
        
        elif prop == 'Length':
            obj.Proxy.length = obj.Length
        
        elif prop == 'Width':
            obj.Proxy.width = obj.Width
        
        if prop == 'Shape':
            box = obj.Shape.BoundBox
            dim = [box.XLength, box.YLength, box.ZLength]
            smallest = min(dim)
            largest = max(dim)
            
            obj.Length = largest
            dim.remove(smallest)
            dim.remove(largest)
            obj.Width = dim[0]
        
    def execute(self, obj):
        ComponentStructural.execute(self, obj)
        self.calc_area_and_thickness(obj)
        
        obj.MassPerArea = obj.Proxy.mass_per_area
        
    def calc_area_and_thickness(self, obj):
        """
        Determine the area and thickness of the plate.
        """
        box = obj.Shape.BoundBox
        
        dim = [ box.XLength, box.YLength, box.ZLength ]
        obj.Thickness = min(dim)
        dim.remove(obj.Thickness)
        obj.Area = dim[0] * dim[1]
   
    