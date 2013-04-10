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
        obj.setEditorMode("Area", 1)
        
        obj.addProperty("App::PropertyFloat", "CriticalFrequency", "Coupling", "Critical frequency.")
        obj.setEditorMode("CriticalFrequency", 1)
        
        obj.addProperty("App::PropertyFloatList", "RadiationEfficiency", "Coupling", "Radiation effiency.")
        obj.setEditorMode("RadiationEfficiency", 1)
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
        