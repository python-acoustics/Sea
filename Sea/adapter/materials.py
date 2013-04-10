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
    
    model = Sea.model.materials.MaterialSolid()
    
    def __init__(self, obj, system):
        baseclasses.Material.__init__(self, obj, system)

        obj.addProperty("App::PropertyFloat", "Young", "Solid", "Young's modulus").Young=0.0
        obj.addProperty("App::PropertyFloat", "Shear", "Solid", "Shear modulus").Shear=0.0
        obj.addProperty("App::PropertyFloat", "Poisson", "Solid", "Poisson's ratio").Poisson=0.0
    
    
    def onChanged(self, obj, prop):
        baseclasses.Material.onChanged(self, obj, prop)
        
        if prop == 'Young':
            obj.Proxy.model.young = obj.Young
        elif prop == 'Shear':
            obj.Proxy.model.shear = obj.Shear
        elif prop == 'Poisson':
            obj.Proxy.model.poisson = obj.Poisson
            
    def execute(self, obj):
        baseclasses.Material.execute(self, obj)
        
class MaterialGas(baseclasses.Material):
    
    name = 'Gas'
    description = 'A material in gas state.'
    
    model = Sea.model.materials.MaterialGas()
    
    def __init__(self, obj, system):
        baseclasses.Material.__init__(self, obj, system)

    
    
    
    
import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
"""