import Sea
from Material import Material

class MaterialGas(Material, Sea.model.materials.MaterialGas):
    
    name = 'Gas'
    description = 'A material in gas state.'
    
    def __init__(self, obj, system):
        Material.__init__(self, obj, system)

    
    
    