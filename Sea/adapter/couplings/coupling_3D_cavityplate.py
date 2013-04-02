import Sea
from .. import baseclasses

class Coupling3DCavityPlate(baseclasses.Coupling):
    """
    A coupling describing the relation between a 3D cavity and a 2D plate.
    """
    name = "CavityToPlate"
    description = "A coupling describing the relation between a cavity and a plate."
    
    def __init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to):
        model = Sea.model.couplings.Coupling3DCavityPlate
        baseclasses.Coupling.__init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to, model)
        
        obj.addProperty("App::PropertyFloat", "Area", "Surface", "Area of the connecting surface.")
        self.calc_area(obj)
        
    def onChanged(self, obj, prop):
        baseclasses.Coupling.onChanged(self, obj, prop)
        
        if prop == 'Area':
            obj.Model.area = obj.Area
        
    def execute(self, obj):
        baseclasses.Coupling.execute(self, obj)
        self.calc_area(self, obj)
    
    def calc_area(self, obj):
        """
        Calculate the connecting surface between the objects.
        """
        comp_from = obj.Document.getObject(obj.ComponentFrom)
        comp_to = obj.Document.getObject(obj.ComponentTo)
        obj.Area = Sea.actions.connection.ShapeConnection(comp_from.Shape, comp_to.Shape).shape().Area
        