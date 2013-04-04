import Sea
from .. import baseclasses

class Coupling3DPlateCavity(baseclasses.Coupling):
    """
    A coupling describing the relation between a 2D plate and a 3D cavity.
    """
    name = "PlateToCavity"
    description = "A coupling describing the relation between a plate and a cavity."
    
    model = Sea.model.couplings.Coupling3DPlateCavity()
    
    def __init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to):
        baseclasses.Coupling.__init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to)
       
        obj.addProperty("App::PropertyFloat", "Area", "Surface", "Area of the connecting surface.")
        self.calc_area(obj)
        
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
        if prop == 'Area':
            obj.Proxy.model.area = obj.Area
        
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
        self.calc_area(obj)
    
    def calc_area(self, obj):
        """
        Calculate the connecting surface between the objects.
        """
        comp_from = obj.Document.getObject(obj.ComponentFrom)
        comp_to = obj.Document.getObject(obj.ComponentTo)
        obj.Area = Sea.actions.connection.ShapeConnection(comp_from.Shape, comp_to.Shape).shape().Area
        