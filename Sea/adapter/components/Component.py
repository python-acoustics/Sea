import abc
import logging
import Sea
import numpy as np

from ..base import Base


class Component(Base):
    """
    Abstract base class for all :mod:`Sea.adapter.components` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :type obj: :class:`FreeCAD.DocumentObject`
        :param system: System instance
        :type system: :class:`Sea.adapter.system.System.System`
        :param material: Material instance
        :type material: :class:`Sea.adapter.materials.Material.Material`
        """
        
        Base.__init__(self, obj)
        
        obj.subsystems = self.subsystems
        
        obj.addProperty("App::PropertyLink", "System", "Component", "System this component belongs to.")
        obj.System = system
        
        obj.makeSubsystem = self.makeSubsystem
        obj.changeMaterial = self.changeMaterial
        
        obj.addProperty("App::PropertyLink", "Material", "Component", "Material the component is made of.")
        obj.Material = material
        
        obj.addProperty("Part::PropertyPartShape", "Shape", "Component", "Shape of Part.")
        obj.setEditorMode("Shape", 1)
        
        obj.addProperty("App::PropertyLinkSub", "VolumeLink", "Component", "Link to volume of component")
        obj.addProperty("App::PropertyFloat", "Volume", "Component", "Volume of component.")
        obj.setEditorMode('Volume', 1)
        obj.addProperty("App::PropertyFloat", "Mass", "Component", "Mass of component.")
        obj.setEditorMode('Mass', 1)
        
        obj.addProperty("App::PropertyStringList", "AvailableSubsystems", "Subsystems", "List of available subsystems for this component.")
        obj.setEditorMode('AvailableSubsystems', 2)
        obj.addProperty("App::PropertyStringList", "EnabledSubsystems", "Subsystems", "List of enabled subsystems for this component.")
        obj.setEditorMode('EnabledSubsystems', 1)
        
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.setEditorMode('Velocity', 1)
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        obj.setEditorMode('VelocityLevel', 1)
        obj.Frequency = system.Frequency
        
        
        obj.AvailableSubsystems = obj.Proxy.availableSubsystems
        #for sort in obj.AvailableSubsystems:   
            #obj.addProperty("App::PropertyLink", "Subsystem" + sort.capitalize(), "Subsystems", "Subsystem of type " + sort)
        obj.EnabledSubsystems = obj.AvailableSubsystems
        
        
        
        
            
    def onChanged(self, obj, prop):
        
        
        if prop == 'System':
            self.system = obj.System.Proxy
        
        if prop == 'Material':
            self.material = obj.Material.Proxy
            
        
        if prop == 'Shape':
            #obj.ViewObject.Proxy=0
            obj.Volume = getattr(obj.Shape, 'Volume')
        
        #if prop == 'VolumeLink':
            #obj.Volume = getattr(obj.Shape, 'Volume')
            
        if prop == 'Volume':
            obj.Proxy.volume = obj.Volume
        
        #if prop == 'Material':
            #obj.Proxy.material = obj.Material.Proxy
        
        if prop == 'Frequency':
            for sub in obj.subsystems():
                sub.Frequency = obj.Frequency
            
        Base.onChanged(self, obj, prop)
        
        
    def execute(self, obj):
        Base.execute(self, obj)
    
        obj.Mass = obj.Proxy.mass
        obj.Velocity = obj.Proxy.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.velocity_level.tolist()
        
    
    @staticmethod
    def subsystems(obj):
        """
        Return a list of subsystems.
        """
        return filter(Sea.actions.document.isSubsystem, obj.InList)    
    
    
    
    @staticmethod
    def makeSubsystem(component, adapter):
        """
        Add a subsystem to a component.
        
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`.
        :param sort: type of subsystem.
        :param model: model of the subsysten belonging to :attr:`component` and specified in :mod:`Sea.components`
        """
                
        obj = component.Document.addObject("App::FeaturePython", "Subsystem")
        adapter(obj, component)
        try:
            Sea.adapter.subsystems.ViewProviderSubsystem(obj.ViewObject)
        except AttributeError:
            pass
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
        component.Proxy.material = material.Proxy.model
        component.Material = material.Name
        
    
    