import abc
from Component import Component
  
class ComponentStructural(Component):
    """
    Abstract base class for all structural component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
     
    def __init__(self, obj, system, material, part):
        Component.__init__(self, obj, system, material)
        #obj.addProperty("App::PropertyFloat", "BendingStiffness", "Component", "Bending stiffness of the Component")
        
        obj.addProperty("App::PropertyFloat", "AreaMomentOfInertia", "Structural", "Area moment of intertia.")
        obj.setEditorMode("AreaMomentOfInertia", 1)
        obj.addProperty("App::PropertyFloat", "RadiusOfGyration", "Structural", "Radius of gyration.")
        obj.setEditorMode("RadiusOfGyration", 1)
        obj.addProperty("App::PropertyLink","Part","Structural", "Reference to Part")
        obj.setEditorMode("Part", 1)
        obj.addProperty("App::PropertyLinkSub", "ShapeLink", "Structural", "Reference to Shape of Part")
        
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.setEditorMode('Velocity', 1)
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        obj.setEditorMode('VelocityLevel', 1)
        
        
        obj.Part = part
        obj.ShapeLink = (obj.Part, ['Shape'])
        
        obj.Label = part.Label + '_' + obj.ClassName
        
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
        if prop == 'Material':
            if obj.Material == None:
                obj.Proxy.material = None
            #else:
                #obj.Proxy.material = obj.Material.Proxy.model
        
        if prop == 'ShapeLink':
            obj.Shape = getattr(obj.Part, 'Shape')
            
    def execute(self, obj):
        Component.execute(self, obj)
        
        obj.AreaMomentOfInertia = obj.Proxy.area_moment_of_inertia
        obj.RadiusOfGyration = obj.Proxy.radius_of_gyration
        obj.Velocity = obj.Proxy.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.velocity_level.tolist()
        
    
  