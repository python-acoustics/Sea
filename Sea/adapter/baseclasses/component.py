import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Component(BaseClass):
    """
    Abstract base class for all Component adapter classes.
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
        
        BaseClass.__init__(self, obj, 'Component')
        system.Components = system.Components + [obj]
        
        
        obj.addProperty("App::PropertyLink", "Material", "Component", "Material the component is made of.")
        obj.addProperty("Part::PropertyPartShape", "Shape", "Component", "Shape of Part.")
       
        obj.addProperty("App::PropertyLinkSub", "VolumeLink", "Component", "Link to volume of component")
        obj.addProperty("App::PropertyFloat", "Volume", "Component", "Volume of component.")
       
        #obj.addProperty("App::PropertyBool", "EnableLong", "Subsystems", "Enable the subsystem describing longitudinal waves.")
        #obj.addProperty("App::PropertyBool", "EnableBend", "Subsystems",, "Enable the subsystem describing bending waves.")
        #obj.addProperty("App::PropertyBool", "EnableShear", "Subsystems", "Enable the subsystem describing shear waves.")
        
        obj.addProperty("App::PropertyStringList", "AvailableSubsystems", "Subsystems", "List of available subsystems for this component.")
        obj.addProperty("App::PropertyStringList", "EnabledSubsystems", "Subsystems", "List of enabled subsystems for this component.")
        
        obj.addProperty("App::PropertyLinkList", "Subsystems", "Subsystems", "List of subsystems.")
        
        
        obj.Material = material
        obj.AvailableSubsystems = self.model.availableSubsystems
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
            self.model.volume = obj.Volume
        
        if prop == 'Material':
            self.model.material = obj.Material.Proxy.model
        
        if prop == 'Frequency':
            for sub in obj.Subsystems:
                sub.Frequency = obj.Frequency
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        #for sort in self.model.availableSubsystems:
            
            ##setattr(obj, sort.capitalize() + 'Impedance', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'impedance'))))
            ##setattr(obj, sort.capitalize() + 'Resistance', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'resistance'))))
            ##setattr(obj, sort.capitalize() + 'Mobility', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'mobility'))))
            
            #setattr(obj, sort.capitalize() + 'ModalDensity', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'modal_density'))))
            #setattr(obj, sort.capitalize() + 'FrequencySpacing', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'average_frequency_spacing'))))
            #setattr(obj, sort.capitalize() + 'SoundspeedPhase', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'soundspeed_phase'))))
            #setattr(obj, sort.capitalize() + 'SoundspeedGroup', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'soundspeed_group'))))
            #setattr(obj, sort.capitalize() + 'DampingTerm', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'damping_term'))))
            #setattr(obj, sort.capitalize() + 'ModalOverlapFactor', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'modal_overlap_factor'))))
    
    ##def includeSubsystem(self, obj, sort):
        ##"""
        ##Include subsystem.
        
        ##:param obj: Feature object
        ##:param sort: string representing type of subsystem, see :attr:`names`.
        ##:param switch: Boolean
        ##"""
        
        ##spectra = { 
                    ##'Impedance' : 'Impedance.',
                    ##'Resistance' : 'Resistance is the real part of the impedance.',
                    ##'Mobility' : 'Mobility.',
                    ##'ModalDensity' : 'Modal density represents the amount of modes per frequency band.',
                    ##'FrequencySpacing' : 'Average frequency spacing in hertz.',
                    ##'SoundspeedPhase' : 'Phase speed of the wave.',
                    ##'SoundspeedGroup' : 'Group speed of the wave.',
                    ##'DampingTerm' : 'Damping term.',
                    ##'ModalOverlapFactor' : 'Modal overlap factor.',
                    ##}

        ##names = { 'bend' : 'Wave - Bending',
                ##'long' : 'Wave - Longitudinal',
                ##'shear' : 'Wave - Shear',
                ##}
        
        ##if sort in names.keys():
            ##for name, description in spectra.iteritems():
                ##obj.addProperty("App::PropertyFloatList", sort.capitalize() + name, names[sort], description)

        ##obj.addProperty("App::PropertyBool", 'Enable' + sort.capitalize(), 'Subsystems', 'Enable subsystem')
        ##setattr(obj, 'Enable' + sort.capitalize(), True)
       
class ComponentStructural(Component):
    """
    Abstract base class for all structural component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
     
    def __init__(self, obj, system, material, part):
        Component.__init__(self, obj, system, material)
        obj.addProperty("App::PropertyFloat", "BendingStiffness", "Component", "Bending stiffness of the Component")
        obj.addProperty("App::PropertyLink","Part","Component", "Reference to Part")
        obj.addProperty("App::PropertyLinkSub", "ShapeLink", "Component", "Reference to Shape of Part")
        
        obj.Part = part
        obj.ShapeLink = (obj.Part, ['Shape'])
        
    
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
        if prop == 'Material':
            if obj.Material == None:
                self.model.material = None
            #else:
                #self.model.material = obj.Material.Proxy.model
        
        if prop == 'ShapeLink':
            obj.Shape = getattr(obj.Part, 'Shape')
            
    def execute(self, obj):
        Component.execute(self, obj)
        
        
        
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
        obj.Shape = Sea.actions.system.getCavity(obj.Structure, obj.Position)
        obj.Volume = obj.Shape.Volume
        