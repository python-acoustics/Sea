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
    
    
    
    def __init__(self, obj, system):
        model = Sea.model.materials.MaterialSolid
        baseclasses.Material.__init__(self, obj, system, model)

        obj.addProperty("App::PropertyFloat", "Young", "Solid", "Young's modulus").Young=0.0
        obj.addProperty("App::PropertyFloat", "Shear", "Solid", "Shear modulus").Shear=0.0
        obj.addProperty("App::PropertyFloat", "Poisson", "Solid", "Poisson's ratio").Poisson=0.0
    
    
    def onChanged(self, obj, prop):
        baseclasses.Material.onChanged(self, obj, prop)
        
        if prop == 'Young':
            obj.Model.young = obj.Young
        elif prop == 'Shear':
            obj.Model.shear = obj.Shear
        elif prop == 'Poisson':
            obj.Model.poisson = obj.Poisson
            
    def execute(self, obj):
        baseclasses.Material.execute(self, obj)
        
class MaterialGas(baseclasses.Material):
    
    name = 'Gas'
    description = 'A material in gas state.'
    
    def __init__(self, obj, system):
        model = Sea.model.materials.MaterialGas
        baseclasses.Material.__init__(self, obj, system, model)

    
    
    
    
import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
"""