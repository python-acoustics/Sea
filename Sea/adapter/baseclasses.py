"""
This following are abstract base classes for the :mod:`adapter` classes.
"""

import abc
import logging
import FreeCAD as App

import FreeCAD, FreeCADGui
from pivy import coin

import Sea

###class ViewProviderBaseClass(object):
    ###"""
    ###Base class for SEA viewprovider
    ###"""
    
    ###def __init__(self, obj):
        ###"""
        ###Set this object to the proxy object of the actual view provider
        ###"""
        ###obj.addProperty("App::PropertyColor","Color","View","Color of the object indicator.")
        ###obj.Proxy = self
        
        ###obj.Color = (1.0,0.0,0.0)
 
    ###def attach(self, obj):
        ###"Setup the scene sub-graph of the view provider, this method is mandatory"

        
        ###self.shaded = coin.SoGroup()
        ###self.wireframe = coin.SoGroup()
        ###self.scale = coin.SoScale()
        ###self.color = coin.SoBaseColor()
        
        ###data=coin.SoCube()
        ###self.shaded.addChild(self.scale)
        ###self.shaded.addChild(self.color)
        ###self.shaded.addChild(data)
        ###obj.addDisplayMode(self.shaded,"Shaded");
        ###style=coin.SoDrawStyle()
        ###style.style = coin.SoDrawStyle.LINES
        ###self.wireframe.addChild(style)
        ###self.wireframe.addChild(self.scale)
        ###self.wireframe.addChild(self.color)
        ###self.wireframe.addChild(data)
        ###obj.addDisplayMode(self.wireframe,"Wireframe");
        ###self.onChanged(obj,"Color")
        ###self.scale.scaleFactor.setValue(10,10,10)
        
 
    ####def updateData(self, fp, prop):
        ####"If a property of the handled feature has changed we have the chance to handle this here"
        ##### fp is the handled feature, prop is the name of the property that has changed
        ####l = fp.getPropertyByName("Length")
        ####w = fp.getPropertyByName("Width")
        ####h = fp.getPropertyByName("Height")
        ####self.scale.scaleFactor.setValue(l,w,h)
        ####pass
 
    ####def getDisplayModes(self,obj):
        ####"Return a list of display modes."
        ####modes=[]
        ####modes.append("Shaded")
        ####modes.append("Wireframe")
        ####return modes
 
    ####def getDefaultDisplayMode(self):
        ####"Return the name of the default display mode. It must be defined in getDisplayModes."
        ####return "Shaded"
 
    ####def setDisplayMode(self,mode):
        ####"Map the display mode defined in attach with those defined in getDisplayModes.\
                ####Since they have the same names nothing needs to be done. This method is optional"
        ####return mode
 
    ###def onChanged(self, vp, prop):
        ###"""
        ###Here we can do something when a single property got changed
        ###"""
        ###FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        ###if prop == "Color":
            ###c = vp.getPropertyByName("Color")
            ###self.color.rgb.setValue(c[0],c[1],c[2])


class BaseClass(object):
    """Abstract base class for all SEA adapters."""
    __metaclass__ = abc.ABCMeta
    
    name = None
    """
    Human-readable name of the object.
    """
    
    description = None
    """
    Description of the object.
    """
    model = None
    """
    Physics :mod:`Sea.model` object of the respective class.
    """
    
    def __init__(self, obj, system, sea_object):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        """
        system.Objects = system.Objects + [obj]
        
        obj.Proxy = self
        
        obj.addProperty("App::PropertyString", "ClassName", "BaseClass", "Name of the class of this object.")
        #obj.addProperty("App::PropertyLink","System","BaseClass", "Reference to System")
        
        obj.addProperty("App::PropertyString", "SeaObject", "SEA", "Type of SEA object.")
        
        obj.SeaObject = sea_object
        
        obj.ClassName = self.__class__.__name__
        #obj.System = system
        
        obj.addProperty("App::PropertyFloatList", "Frequency", "BaseClass", "Frequency bands")
        

    def __del__(self):
        logging.info("Object - Destructor - Deleting this object")        
        
    def onChanged(self, obj, prop):
        """
        Respond on a change in object :attr:`obj` to property :attr:`prop`.
        
        :param obj: Feature object
        :param prop: Property that was updated
        """
        logging.info("Object %s - onChanged - Changing property %s.", obj.Name, prop)
        
        if prop == 'Frequency':
            self.model.frequency = obj.Frequency
            
    def execute(self, obj):
        """
        This method will be executed on a recomputation.
        
        :param obj: Feature object
        """
        pass
        #obj.Frequency = (obj.System.Name, ['Frequency'])


class Component(BaseClass):
    """
    Abstract base class for all Component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        :param material: Material instance as defined in :mod:`Sea.adapter.materials`
        :param material: FreeCAD part
        """
        
        BaseClass.__init__(self, obj, system, 'Component')
        
        
        obj.addProperty("App::PropertyLinkSub", "Volume", "SeaComponent", "Volume of component")
       
        #obj.addProperty("App::PropertyBool", "EnableLong", "Subsystems", "Enable the subsystem describing longitudinal waves.")
        #obj.addProperty("App::PropertyBool", "EnableBend", "Subsystems", "Enable the subsystem describing bending waves.")
        #obj.addProperty("App::PropertyBool", "EnableShear", "Subsystems", "Enable the subsystem describing shear waves.")
        
        obj.addProperty("App::PropertyStringList", "AvailableSubsystems", "Subsystems", "List of available subsystems for this component.")
        obj.addProperty("App::PropertyStringList", "EnabledSubsystems", "Subsystems", "List of enabled subsystems for this component.")
        
        #obj.Volume = (obj.Part, ['Shape', 'Volume'])
        
        obj.AvailableSubsystems = self.model.availableSubsystems
        for sort in obj.AvailableSubsystems:
            self.includeSubsystem(obj, sort)
        
   
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        
        if prop == 'Shape':
            obj.ViewObject.Proxy=0
        
        if prop == 'Volume':
            self.model.volume = obj.Volume
        
        #elif prop == 'EnableLong':
            #self.enableSubsystem(obj, 'long', obj.EnableLong)
        
        #elif prop == 'EnableBend':
            #self.enableSubsystem(obj, 'bend', obj.EnableBend)
        
        #elif prop == 'EnableShear':
            #self.enableSubsystem(obj, 'shear', obj.EnableShear)
        

    def execute(self, obj):
        BaseClass.execute(self, obj)
    
        #for sort in self.availableSubsystems:
            #setattr(obj, sort.capitalize() + 'Impedance', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'impedance'))))
            #setattr(obj, sort.capitalize() + 'Resistance', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'resistance'))))
            #setattr(obj, sort.capitalize() + 'Mobility', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'mobility'))))
            #setattr(obj, sort.capitalize() + 'ModalDensity', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'modal_density'))))
            #setattr(obj, sort.capitalize() + 'FrequencySpacing', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'average_frequency_spacing'))))
            #setattr(obj, sort.capitalize() + 'SoundspeedPhase', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'soundspeed_phase'))))
            #setattr(obj, sort.capitalize() + 'SoundspeedGroup', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'soundspeed_group'))))
            #setattr(obj, sort.capitalize() + 'DampingTerm', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'damping_term'))))
            #setattr(obj, sort.capitalize() + 'ModalOverlapFactor', map(float, list(getattr(getattr(self.model, 'subsystem_' + sort), 'modal_overlap_factor'))))
    
    def includeSubsystem(self, obj, sort):
        """
        Include subsystem.
        
        :param obj: Feature object
        :param sort: string representing type of subsystem, see :attr:`names`.
        :param switch: Boolean
        """
        
        spectra = { 
                    'Impedance' : 'Impedance.',
                    'Resistance' : 'Resistance is the real part of the impedance.',
                    'Mobility' : 'Mobility.',
                    'ModalDensity' : 'Modal density represents the amount of modes per frequency band.',
                    'FrequencySpacing' : 'Average frequency spacing in hertz.',
                    'SoundspeedPhase' : 'Phase speed of the wave.',
                    'SoundspeedGroup' : 'Group speed of the wave.',
                    'DampingTerm' : 'Damping term.',
                    'ModalOverlapFactor' : 'Modal overlap factor.',
                    }

        names = { 'bend' : 'Wave - Bending',
                'long' : 'Wave - Longitudinal',
                'shear' : 'Wave - Shear',
                }
        
        if sort in names.keys():
            for name, description in spectra.iteritems():
                obj.addProperty("App::PropertyFloatList", sort.capitalize() + name, names[sort], description)

        obj.addProperty("App::PropertyBool", 'Enable' + sort.capitalize(), 'Subsystems', 'Enable subsystem')
        setattr(obj, 'Enable' + sort.capitalize(), True)
        
    #def enableSubsystem(self, obj, sort, switch):
        #"""
        #Enable subsystem.
        
        #:param obj: Feature object
        #:param sort: string representing type of subsystem, see :attr:`names`.
        #:param switch: Boolean
        #"""
        
        #spectra = { 
                    #'Impedance' : 'Impedance.',
                    #'Resistance' : 'Resistance is the real part of the impedance.',
                    #'Mobility' : 'Mobility.',
                    #'ModalDensity' : 'Modal density represents the amount of modes per frequency band.',
                    #'FrequencySpacing' : 'Average frequency spacing in hertz.',
                    #'SoundspeedPhase' : 'Phase speed of the wave.',
                    #'SoundspeedGroup' : 'Group speed of the wave.',
                    #}

        #names = { 'bend' : 'Wave - Bending',
                #'long' : 'Wave - Longitudinal',
                #'shear' : 'Wave - Shear',
                #}
        
        #if sort in names.keys():
            #if switch:
                #for name, description in spectra.iteritems():
                    #obj.addProperty("App::PropertyFloatList", sort.capitalize() + name, names[sort], description)
            #else:
                #for name in spectra.iterkeys():
                    #obj.removeProperty(sort.capitalize() + name)


       
class ComponentStructural(Component):
    """
    Abstract base class for all structural component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    availableSubsystems = ['long', 'bend', 'shear']
    
    def __init__(self, obj, system, material, part):
        Component.__init__(self, obj, system)
        obj.addProperty("App::PropertyFloat", "BendingStiffness", "Component", "Bending stiffness of the Component")
        
        
        obj.addProperty("App::PropertyLink","Part","Component", "Reference to Part")
        obj.addProperty("App::PropertyLink","Material","Component", "Reference to Material")
        obj.addProperty("App::PropertyLinkSub", "ShapeLink", "Component", "Reference to Shape of Part")
        obj.addProperty("Part::PropertyPartShape", "Shape", "Component", "Shape of Part.")
        
        obj.Part = part
        obj.Material = material
        
        
        
        
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
    
    
    
    def __init__(self, obj, system, position):
        Component.__init__(self, obj, system)
        
        obj.addProperty("App::PropertyVector", "Position", "Cavity", "Position within the cavity.")
        obj.addProperty("Part::PropertyPartShape", "Shape", "Shape", "Shape of the cavity.")
        obj.addProperty("App::PropertyLink", "Structure", "Structure", "Fused structure.")
        
        obj.Structure = system.Structure
        obj.Position = position
        
        self.includeSubsystem(obj, 'long')
        obj.EnableLong = True
        self.execute(obj)
        
    def onChanged(self, obj, prop):
        Component.onChanged(self, obj, prop)
        
    def execute(self, obj):
        Component.execute(self, obj)
        self.updateCavity(obj)
        
    def updateCavity(self, obj):
        """
        Update the Shape of the Cavity.
        """
        obj.Shape = Sea.actions.system.getCavity(obj.Structure, obj.Position)
        #print obj.Shape.Volume
        
        
class Material(BaseClass):
    """
    Abstract base class for all Material adapter classes.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, obj, system):
        BaseClass.__init__(self, obj, system, 'Material')
        
        obj.addProperty("App::PropertyFloat", "Density", "Material", "Density of the material.")
        obj.addProperty("App::PropertyFloat", "LossFactor", "Material", "Loss factor of the material.")
        obj.addProperty("App::PropertyFloat", "Temperature", "Material", "Temperature of the material.")
        obj.addProperty("App::PropertyFloat", "Pressure", "Material", "Pressure of the material.")
        

    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'Density':
            self.model.density = obj.Density
        elif prop == 'LossFactor':
            self.model.loss_factor = obj.LossFactor
        elif prop == 'Temperature':
            self.model.temperature = obj.Temperature
        elif prop == 'Pressure':
            self.model.pressure = obj.Pressure
        
        
    def execute(self, obj):
        pass

        
class Coupling(BaseClass):
    """
    Abstract base class for couplings.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, connection, component_from, subsystem_from, component_to, subsystem_to):
        BaseClass.__init__(self, obj, system, 'Coupling')
        
        obj.addProperty("App::PropertyFloatList", "CLF", "Coupling", "Coupling loss factor.")
        
        obj.addProperty("App::PropertyLink", "Connection", "Coupling", "Connection this coupling is part of.")
        obj.addProperty("App::PropertyLink", "ComponentFrom", "Coupling", "Component from")
        obj.addProperty("App::PropertyLink", "ComponentTo", "Coupling", "Component to")
        obj.addProperty("App::PropertyString", "SubsystemFrom", "Coupling", "Subsystem from")
        obj.addProperty("App::PropertyString", "SubsystemTo", "Coupling", "Subsystem to")
        
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceFrom", "Subsystem From", "Impedance of connection corrected From subsystem.")     
        obj.addProperty("App::PropertyFloatList", "ResistanceFrom", "Subsystem From", "Resistance of connection corrected From subsystem.")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceTo", "Subsystem To", "Impedance of connection corrected To subsystem.")
        obj.addProperty("App::PropertyFloatList", "ResistanceTo", "Subsystem To", "Resistance of connection corrected To subsystem.")
        
        
        """How or more specifically, when to update the size of the coupling?"""
        obj.addProperty("App::PropertyFloat", "Size", "Coupling", "Size of the junction.")
        
        
        obj.Connection = connection
        obj.ComponentFrom = component_from
        obj.ComponentTo = component_to
        obj.SubsystemFrom = subsystem_from
        obj.SubsystemTo = subsystem_to
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        #pass
        #if prop == 'Connection':
            #self.model.connection = obj.Connection.Proxy.model
        
        #elif prop == 'ComponentFrom' or 'SubsystemFrom':
            #self.model.component_from = Obj.ComponentFrom.Proxy.model
            #self.model.subsystem_from = getattr(Obj.ComponentFrom.Proxy.model, 'subsystem_' + Obj.SubsystemFrom)
            
        #elif prop == 'ComponentTo' or 'SubsystemTo':
            #self.model.component_to = Obj.ComponentTo.Proxy.model
            #self.model.subsystem_to = getattr(Obj.ComponentTo.Proxy.model, 'subsystem_' + Obj.SubsystemTo)
            

    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        obj.CLF = self.model.clf
        
        obj.ImpedanceFrom = self.model.impedance_from
        obj.ImpedanceTo = self.model.impedance_to
        obj.ResistanceFrom = self.model.resistance_from
        obj.ResistanceTo = self.model.resistance_to
    
    
    #@abc.abstractmethod
    #def size(self, obj):
        #"""
        #Return the size of the coupling.
        #"""
        #return
            
class Excitation(BaseClass):
    """
    Abstract base class for all Excitation adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init___(self, obj, system, subsystem, **properties):
        BaseClass.__init__(self, obj, system, 'Excitation')
        
        obj.addProperty("App::PropertyLink", "Subsystem", "Excitation", "Subsystem that is excited.")  
        
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Subsystem = subsystem
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)  
        
        if prop == 'Subsystem':
            self.model.subsystem = obj.Subsystem.Proxy.model