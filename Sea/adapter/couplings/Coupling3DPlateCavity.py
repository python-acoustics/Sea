import Sea
from Coupling import Coupling

class Coupling3DPlateCavity(Coupling, Sea.model.couplings.Coupling3DPlateCavity):
    """
    A coupling describing the relation between a 2D plate and a 3D cavity.
    """
    name = "PlateToCavity"
    description = "A coupling describing the relation between a plate and a cavity."
    
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
        comp_from = obj.Document.getObject(obj.ComponentFrom)
        comp_to = obj.Document.getObject(obj.ComponentTo)
        obj.Area = Sea.actions.connection.ShapeConnection(comp_from.Shape, comp_to.Shape).shape().Area
        