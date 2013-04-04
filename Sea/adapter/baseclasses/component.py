import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Component(BaseClass):
    """
    Abstract base class for all :mod:`Sea.adapter.components` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        :param material: Material instance as defined in :mod:`Sea.adapter.materials`
        :param material: FreeCAD part
        """
        
        BaseClass.__init__(self, obj)
        system.Components = system.Components + [obj]
        
        
        obj.makeSubsystem = self.makeSubsystem
        obj.changeMaterial = self.changeMaterial
        
        obj.addProperty("App::PropertyString", "Material", "Component", "Material the component is made of.")
        obj.Material = material.Name
        
        obj.addProperty("Part::PropertyPartShape", "Shape", "Component", "Shape of Part.")
       
        obj.addProperty("App::PropertyLinkSub", "VolumeLink", "Component", "Link to volume of component")
        obj.addProperty("App::PropertyFloat", "Volume", "Component", "Volume of component.")
       
        #obj.addProperty("App::PropertyBool", "EnableLong", "Subsystems", "Enable the subsystem describing longitudinal waves.")
        #obj.addProperty("App::PropertyBool", "EnableBend", "Subsystems",, "Enable the subsystem describing bending waves.")
        #obj.addProperty("App::PropertyBool", "EnableShear", "Subsystems", "Enable the subsystem describing shear waves.")
        
        obj.addProperty("App::PropertyStringList", "AvailableSubsystems", "Subsystems", "List of available subsystems for this component.")
        obj.addProperty("App::PropertyStringList", "EnabledSubsystems", "Subsystems", "List of enabled subsystems for this component.")
        
        obj.addProperty("App::PropertyLinkList", "Subsystems", "Subsystems", "List of subsystems.")
        
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        
        obj.Frequency = system.Frequency
        
        material.Components = material.Components + [obj]
        obj.Proxy.model.material = material.Proxy.model
        obj.Material = material.Name
        
        obj.AvailableSubsystems = obj.Proxy.model.availableSubsystems
        for sort in obj.AvailableSubsystems:   
            obj.addProperty("App::PropertyLink", "Subsystem" + sort.capitalize(), "Subsystems", "Subsystem of type " + sort)
        obj.EnabledSubsystems = obj.AvailableSubsystems
        
        
        
        
            
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        
        if prop == 'Shape':
            #obj.ViewObject.Proxy=0
            obj.Volume = getattr(obj.Shape, 'Volume')
        
        #if prop == 'VolumeLink':
            #obj.Volume = getattr(obj.Shape, 'Volume')
            
        if prop == 'Volume':
            obj.Proxy.model.volume = obj.Volume
        
        #if prop == 'Material':
            #obj.Proxy.model.material = obj.Material.Proxy.model
        
        if prop == 'Frequency':
            for sub in obj.Subsystems:
                sub.Frequency = obj.Frequency
        
        if prop == 'Subsystems':
            obj.Proxy.model.linked_subsystems = [subsystem.Proxy.model for subsystem in obj.Subsystems]
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
    
        obj.Velocity = obj.Proxy.model.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.model.velocity_level.tolist()
        
    @staticmethod
    def makeSubsystem(component, adapter):
        """
        Add a subsystem to a component.
        
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`.
        :param sort: type of subsystem.
        :param model: model of the subsysten belonging to :attr:`component` and specified in :mod:`Sea.model.components`
        """
                
        obj = component.newObject("App::DocumentObjectGroupPython", "Subsystem")
        
        adapter(obj, component)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj  
    
    @staticmethod
    def changeMaterial(component, material):
        """
        Change material of :attr:`component` to :attr:`material`.
        """
        import FreeCAD as App
        old_material = App.ActiveDocument.getObject(component.Material)
        old_components = old_material.Components
        old_components.remove(component)
        old_material.Components = old_components
        material.Components = material.Components + [component]
        component.Proxy.model.material = material.Proxy.model
        component.Material = material.Name
        
    
    
class ComponentStructural(Component):
    """
    Abstract base class for all structural component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
     
    def __init__(self, obj, system, material, part):
        Component.__init__(self, obj, system, material)
        #obj.addProperty("App::PropertyFloat", "BendingStiffness", "Component", "Bending stiffness of the Component")
        
        obj.addProperty("App::PropertyFloat", "AreaMomentOfInertia", "Structural", "Area moment of intertia.")
        obj.addProperty("App::PropertyFloat", "RadiusOfGyration", "Structural", "Radius of gyration.")
        obj.addProperty("App::PropertyLink","Part","Structural", "Reference to Part")
        obj.addProperty("App::PropertyLinkSub", "ShapeLink", "Structural", "Reference to Shape of Part")
        
        obj.Part = part
        obj.ShapeLink = (obj.Part, ['Shape'])
        
        obj.Label = part.Label + '_' + obj.ClassName
        
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
        if prop == 'Material':
            if obj.Material == None:
                obj.Proxy.model.material = None
            #else:
                #obj.Proxy.model.material = obj.Material.Proxy.model
        
        if prop == 'ShapeLink':
            obj.Shape = getattr(obj.Part, 'Shape')
            
    def execute(self, obj):
        Component.execute(self, obj)
        
        obj.AreaMomentOfInertia = obj.Proxy.model.area_moment_of_inertia
        obj.RadiusOfGyration = obj.Proxy.model.radius_of_gyration
        
        
class ComponentCavity(Component):
    """
    Abstract base class for all cavity component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material, position):
        Component.__init__(self, obj, system, material)
        
        obj.addProperty("App::PropertyVector", "Position", "Cavity", "Position within the cavity.")
        obj.addProperty("App::PropertyLink", "Structure", "Structure", "Fused structure.")
        
        obj.Structure = system.Structure
        obj.Position = position
        self.execute(obj)
        
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
    def execute(self, obj):
        self.updateCavity(obj)
        Component.execute(self, obj)
        
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
    
    