import Sea
from Coupling import Coupling

class Coupling3DCavityPlate(Coupling, Sea.model.couplings.Coupling3DCavityPlate):
    """
    A coupling describing the relation between a 3D cavity and a 2D plate.
    """
    name = "CavityToPlate"
    description = "A coupling describing the relation between a cavity and a plate."
    
    def __init__(self, obj, connection, subsystem_from, subsystem_to):
        Coupling.__init__(self, obj, connection, subsystem_from, subsystem_to)
        
        obj.addProperty("App::PropertyFloat", "Area", "Surface", "Area of the connecting surface.")
        self.calc_area(obj)
        
    def onChanged(self, obj, prop):
        Coupling.onChanged(self, obj, prop)
        
        if prop == 'Area':
            obj.Proxy.area = obj.Area
        
    def execute(self, obj):
        Coupling.execute(self, obj)
        self.calc_area(obj)
    
    def calc_area(self, obj):
        """
        Calculate the connecting surface between the objects.
        """
        shape_from = obj.SubsystemFrom.Component.Shape
        shape_to = obj.SubsystemTo.Component.Shape
        obj.Area = Sea.actions.connection.ShapeConnection(shape_from, shape_to).shape().Area
        