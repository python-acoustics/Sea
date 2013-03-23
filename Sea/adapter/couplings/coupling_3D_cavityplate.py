import Sea
from .. import baseclasses

class Coupling3DCavityPlate(baseclasses.Coupling):
    """
    A coupling describing the relation between a 3D cavity and a 2D plate.
    """
    name = "CavityToPlate"
    description = "A coupling describing the relation between a cavity and a plate."
    
    model = Sea.model.couplings.Coupling3DCavityPlate()
    
    def __init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to)
        
        obj.addProperty("App::PropertyFloat", "Area", "Surface", "Area of the connecting surface.")
        self.calc_area(obj)
        
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
        if prop == 'Area':
            self.model.area = obj.Area
        
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
        self.calc_area(self, obj)
    
    def calc_area(self, obj):
        """
        Calculate the connecting surface between the objects.
        """
        obj.Area = Sea.actions.connection.ShapeConnection(obj.ComponentFrom.Shape, obj.ComponentTo.Shape).shape().Area
        