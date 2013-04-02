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
    
    def __init__(self, obj, system, material, model):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        :param material: Material instance as defined in :mod:`Sea.adapter.materials`
        :param material: FreeCAD part
        """
        
        BaseClass.__init__(self, obj, model)
        system.Components = system.Components + [obj]
        
        obj.makeSubsystem = self.makeSubsystem
        
        #obj.addProperty("App::PropertyLink", "Material", "Component", "Material the component is made of.")
        obj.addProperty("Part::PropertyPartShape", "Shape", "Component", "Shape of Part.")
       
        obj.addProperty("App::PropertyLinkSub", "VolumeLink", "Component", "Link to volume of component")
        obj.addProperty("App::PropertyFloat", "Volume", "Component", "Volume of component.")
       
        #obj.addProperty("App::PropertyBool", "EnableLong", "Subsystems", "Enable the subsystem describing longitudinal waves.")
        #obj.addProperty("App::PropertyBool", "EnableBend", "Subsystems",, "Enable the subsystem describing bending waves.")
        #obj.addProperty("App::PropertyBool", "EnableShear", "Subsystems", "Enable the subsystem describing shear waves.")
        
        obj.addProperty("App::PropertyStringList", "AvailableSubsystems", "Subsystems", "List of available subsystems for this component.")
        obj.addProperty("App::PropertyStringList", "EnabledSubsystems", "Subsystems", "List of enabled subsystems for this component.")
        
        obj.addProperty("App::PropertyLinkList", "Subsystems", "Subsystems", "List of subsystems.")
        
        
        #obj.Material = material
        
        material.Components = material.Components + [obj]
        obj.Model.material = material.Model
        
        obj.AvailableSubsystems = obj.Model.availableSubsystems
        for sort in obj.AvailableSubsystems:   
            obj.addProperty("App::PropertyLink", "Subsystem" + sort.capitalize(), "Subsystems", "Subsystem of type " + sort)
        obj.EnabledSubsystems = obj.AvailableSubsystems
        obj.Frequency = system.Frequency
        
            
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        
        if prop == 'Shape':
            #obj.ViewObject.Proxy=0
            obj.Volume = getattr(obj.Shape, 'Volume')
        
        #if prop == 'VolumeLink':
            #obj.Volume = getattr(obj.Shape, 'Volume')
            
        if prop == 'Volume':
            obj.Model.volume = obj.Volume
        
        #if prop == 'Material':
            #obj.Model.material = obj.Material.Model
        
        if prop == 'Frequency':
            for sub in obj.Subsystems:
                sub.Frequency = obj.Frequency
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
    
    @staticmethod
    def makeSubsystem(component, sort, model):
        """
        Add a subsystem to a component.
        
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`.
        :param sort: type of subsystem.
        :param model: model of the subsysten belonging to :attr:`component` and specified in :mod:`Sea.model.components`
        """
        from Sea.adapter.object_maps import subsystems_map
        
        obj = component.newObject("App::FeaturePython", "Subsystem")
        subsystems_map[sort](obj, component, model)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj  
       
class ComponentStructural(Component):
    """
    Abstract base class for all structural component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
     
    def __init__(self, obj, system, material, part, model):
        Component.__init__(self, obj, system, material, model)
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
                obj.Model.material = None
            #else:
                #obj.Model.material = obj.Material.Model
        
        if prop == 'ShapeLink':
            obj.Shape = getattr(obj.Part, 'Shape')
            
    def execute(self, obj):
        Component.execute(self, obj)
        
        obj.AreaMomentOfInertia = obj.Model.area_moment_of_inertia
        obj.RadiusOfGyration = obj.Model.radius_of_gyration
        
        
class ComponentCavity(Component):
    """
    Abstract base class for all cavity component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material, position, model):
        Component.__init__(self, obj, system, material, model)
        
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
        obj.Shape = Sea.actions.system.getCavity(obj.Structure, obj.Position)
        obj.Volume = obj.Shape.Volume
        