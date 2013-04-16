import abc
from Component import Component
        
class ComponentCavity(Component):
    """
    Abstract base class for all cavity component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material, position):
        Component.__init__(self, obj, system, material)
        
        obj.addProperty("App::PropertyVector", "Position", "Cavity", "Position within the cavity.")
        obj.setEditorMode("Position", 1)
        obj.addProperty("App::PropertyLink", "Structure", "Structure", "Fused structure.")
        obj.setEditorMode("Structure", 2)
        
        obj.addProperty("App::PropertyFloatList", "Pressure", "Subsystem", "Mean pressure.")
        obj.setEditorMode('Pressure', 1)
        obj.addProperty("App::PropertyFloatList", "PressureLevel", "Subsystem", "Pressure level.")
        obj.setEditorMode('PressureLevel', 1)
        
        
        obj.Structure = system.Structure
        obj.Position = position
        self.execute(obj)
        
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
    def execute(self, obj):
        self.updateCavity(obj)
        Component.execute(self, obj)
        
        obj.Pressure = obj.Proxy.pressure.tolist()
        obj.PressureLevel = obj.Proxy.pressure_level.tolist()
        
        
    def updateCavity(self, obj):
        """
        Update the Shape of the Cavity.
        """
        obj.Shape = self.getCavityShape(obj.Structure, obj.Position)
        obj.Volume = obj.Shape.Volume
    
    @staticmethod
    def getCavityShape(structure, position):
        """
        Return shape of cavity in structure for a certain position.
        
        :param structure: a :class:`Part.MultiFuse`
        :param position: a :class:`FreeCAD.Vector`
        
        :rtype: :class:`FreeCAD.TopoShape`
        """
        #structure = obj.Structure
        tolerance = 0.01
        allowface = False
            
        for shape in structure.Shape.Shells:
            if shape.isInside(position, tolerance, allowface) and shape.Volume < 0.0:
                shape.complement() # Reverse the shape to obtain positive volume
                return shape
            #else:
                #App.Console.PrintWarning("No cavity at this position.\n")
    
