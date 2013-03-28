"""
Adapter classes for :class:`Sea.model.components.Component2DPlate`
"""

import Sea
from .. import baseclasses

class Component2DPlate(baseclasses.ComponentStructural):
    """
    Plate structural component.
    """

    name = 'Plate'
    description = 'A structural component with wave propagation along two dimensions.'
    
    model = Sea.model.components.Component2DPlate()  
    """
    This adapter describes a :class:`Sea.model.components.Component2DPlate`
    """
    
    def __init__(self, obj, system, material, part):
        baseclasses.ComponentStructural.__init__(self, obj, system, material, part)
        
        obj.addProperty("App::PropertyFloat", "Area", self.name, "Area of the plate.")
        obj.addProperty("App::PropertyFloat", "Thickness", self.name, "Thickness of the plate.")
        obj.addProperty("App::PropertyFloat", "MassPerArea", self.name, "Mass per unit area.")
        self.calc_area_and_thickness(obj)
        
        
        obj.SubsystemLong = Sea.actions.factory.makeSubsystem(obj, 'SubsystemLong', Sea.model.components.structural_2D_plate.SubsystemLong)
        obj.SubsystemBend = Sea.actions.factory.makeSubsystem(obj, 'SubsystemBend', Sea.model.components.structural_2D_plate.SubsystemBend) 
        obj.SubsystemShear = Sea.actions.factory.makeSubsystem(obj, 'SubsystemShear', Sea.model.components.structural_2D_plate.SubsystemShear) 
        
        
    def onChanged(self, obj, prop):
        baseclasses.ComponentStructural.onChanged(self, obj, prop)
        
        if prop == 'Area':
            self.model.area = obj.Area
        
        if prop == 'Thickness':
            self.model.thickness = obj.Thickness
            
    def execute(self, obj):
        baseclasses.ComponentStructural.execute(self, obj)
        self.calc_area_and_thickness(obj)
        
        obj.MassPerArea = self.model.mass_per_area
        
    def calc_area_and_thickness(self, obj):
        """
        Determine the area and thickness of the plate.
        """
        box = obj.Shape.BoundBox
        
        dim = [ box.XLength, box.YLength, box.ZLength ]
        obj.Thickness = min(dim)
        dim.remove(obj.Thickness)
        obj.Area = dim[0] * dim[1]
   
    