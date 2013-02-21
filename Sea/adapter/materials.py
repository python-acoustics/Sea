"""
The following are Material classes encapsulating their respective :mod:`Sea.model.materials` class.
"""

import logging

import Sea
import baseclasses

class MaterialSolid(baseclasses.Material):
    """
    Solid material
    """
    name = 'Solid'
    description = 'A material in solid state.'
    
    model = Sea.model.MaterialSolid()
    
    def __init__(self, obj, system, **properties):
        baseclasses.Material.__init__(self, obj, system, **properties)

        obj.addProperty("App::PropertyFloat", "Young", "Solid", "Young's modulus")
        obj.addProperty("App::PropertyFloat", "Bulk", "Solid", "Bulk modulus")
        obj.addProperty("App::PropertyFloat", "Shear", "Solid", "Shear modulus")
        obj.addProperty("App::PropertyFloat", "Poisson", "Solid", "Poisson's ratio")
    
    
    def onChanged(self, obj, prop):
        baseclasses.Material.onChanged(self, obj, prop)
        
        if prop == 'Young':
            self.model.young = obj.Young
        elif prop == 'Bulk':
            self.model.bulk = obj.Bulk
        elif prop == 'Shear':
            self.model.shear = obj.Shear
        elif prop == 'Poisson':
            self.model.poisson = obj.Poisson
            
    def execute(self, obj):
        baseclasses.Material.execute(self, obj)

        obj.Young = self.model.young if self.model.young else 0.0
    

import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
"""