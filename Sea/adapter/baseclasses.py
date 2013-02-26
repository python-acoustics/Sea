"""
This following are abstract base classes for the :mod:`adapter` classes.
"""

import abc
import logging
import FreeCAD as App

import FreeCAD, FreeCADGui
from pivy import coin


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
    
    def __init__(self, obj, system):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        """
        
        obj.Proxy = self
        
        obj.addProperty("App::PropertyLink","System","BaseClass", "Reference to System")
        obj.System = system
        
        obj.addProperty("App::PropertyLinkSub", "Frequency", "BaseClass", "Frequency bands")
        
        obj.Frequency = (system, ['Frequency'])
        

    def __del__(self):
        logging.info("Object - Destructor - Deleting this object")        
        
    def onChanged(self, obj, prop):
        """
        Respond on a change in object :attr:`obj` to property :attr:`prop`.
        
        :param obj: Feature object
        :param prop: Property that was updated
        """
        logging.info("Object %s - onChanged - Changing property %s.", obj.Name, prop)
        
        if prop == 'System':
            if obj.System == None:
                self.model.system = None
            else:
                self.model.system = obj.System.Proxy.model
        elif prop == 'Frequency':
            self.model.frequency = obj.Frequency
            
    def execute(self, obj):
        """
        This method will be executed on a recomputation.
        
        :param obj: Feature object
        """
        obj.Frequency = (obj.System.Name, ['Frequency'])


class Component(BaseClass):
    """
    Abstract base class for all Component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material, part):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        :param material: Material instance as defined in :mod:`Sea.adapter.materials`
        :param material: FreeCAD part
        :param **properties: Properties
        """
        
        
        BaseClass.__init__(self, obj, system)
        
        obj.addProperty("App::PropertyBool","IsSeaComponent","Component", "True if it is a valid SEA Component")        
        obj.setEditorMode("IsSeaComponent", 2)
        
        obj.addProperty("App::PropertyLink","Part","Component", "Reference to Part")
        obj.addProperty("App::PropertyLink","Material","Component", "Reference to Material")

        
        obj.addProperty("App::PropertyLinkSub", "Volume", "SeaComponent", "Volume of component")
       
        obj.addProperty("App::PropertyBool", "EnableLong", "Subsystems", "Enable the subsystem describing longitudinal waves.")
        obj.addProperty("App::PropertyBool", "EnableBend", "Subsystems", "Enable the subsystem describing bending waves.")
        obj.addProperty("App::PropertyBool", "EnableShear", "Subsystems", "Enable the subsystem describing shear waves.")
        

        obj.IsSeaComponent = True
        obj.Part = part
        obj.Material = material
        
        #obj.Volume = (obj.Part, ['Shape', 'Volume'])
   
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'Material':
            if obj.Material == None:
                self.model.material = None
            #else:
                #self.model.material = obj.Material.Proxy.model
        
        elif prop == 'Part':
            if obj.Part == None:
                obj.Volume = None
            else:
                obj.Volume = (obj.Part, ['Shape', 'Volume'])
                
        elif prop == 'Volume':
            self.model.volume = obj.Volume
        
        #elif prop == 'EnableLong':
            #self.enableSubsystem(obj, 'long', obj.EnableLong)
        
        #elif prop == 'EnableBend':
            #self.enableSubsystem(obj, 'bend', obj.EnableBend)
        
        #elif prop == 'EnableShear':
            #self.enableSubsystem(obj, 'shear', obj.EnableShear)
        

    def execute(self, obj):
        BaseClass.execute(self, obj)
    
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
                    }

        names = { 'bend' : 'Wave - Bending',
                'long' : 'Wave - Longitudinal',
                'shear' : 'Wave - Shear',
                }
        
        if sort in names.keys():
            for name, description in spectra.iteritems():
                obj.addProperty("App::PropertyFloatList", sort.capitalize() + name, names[sort], description)

                    
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
        Component.__init__(self, obj, system, material, part)
        obj.addProperty("App::PropertyFloat", "BendingStiffness", "Component", "Bending stiffness of the Component")
        
        for sort in self.availableSubsystems:
            self.includeSubsystem(obj, sort)
        
        obj.EnableLong = True
        obj.EnableBend = True
        obj.EnableShear = True
    
    
    def execute(self, obj):
        Component.execute(self, obj)
        
        for sort in self.availableSubsystems:
            setattr(obj, sort.capitalize() + 'Impedance', getattr(getattr(self, 'subsystem_' + sort), 'impedance'))
            setattr(obj, sort.capitalize() + 'Resistance', getattr(getattr(self, 'subsystem_' + sort), 'resistance'))
            setattr(obj, sort.capitalize() + 'Mobility', getattr(getattr(self, 'subsystem_' + sort), 'mobility'))
            setattr(obj, sort.capitalize() + 'ModalDensity', getattr(getattr(self, 'subsystem_' + sort), 'modal_density'))
            setattr(obj, sort.capitalize() + 'FrequencySpacing', getattr(getattr(self, 'subsystem_' + sort), 'average_frequency_spacing'))
            setattr(obj, sort.capitalize() + 'SoundspeedPhase', getattr(getattr(self, 'subsystem_' + sort), 'soundspeed_phase'))
            setattr(obj, sort.capitalize() + 'SoundspeedGroup', getattr(getattr(self, 'subsystem_' + sort), 'soundspeed_group'))

class ComponentCavity(Component):
    """
    Abstract base class for all cavity component adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, material, part):
        Component.__init__(self, obj, system, material, part)
        
        self.includeSubsystem(obj, 'long')
        obj.EnableLong = True
        
class Material(BaseClass):
    """
    Abstract base class for all Material adapter classes.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, obj, system, **properties):
        BaseClass.__init__(self, obj, system)
        
        obj.addProperty("App::PropertyBool","IsSeaMaterial","Material", "True if it is a valid SEA Material").IsSeaMaterial=True        
        obj.setEditorMode("IsSeaMaterial", 2)
        
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
    Abstract base class for all Coupling adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, system, subsystem_from, subsystem_to, **properties):
        BaseClass.__init__(self, obj, system)
            
        obj.addProperty("App::PropertyBool","IsSeaCoupling","Coupling", "True if it is a valid SEA Coupling").IsSeaCoupling=True        
        obj.setEditorMode("IsSeaCoupling", 2)
        
        
        obj.addProperty("App::PropertyLink", "Components", "Coupling", "Components that are connected via this coupling.")
        
        obj.addProperty("App::PropertyLink", "Subsystems", "Coupling", "Components that are connected via this coupling.")
        
        #obj.addProperty("App::PropertyLink", "SubsystemFrom", "Subsystem", "Subsystem the coupling begins.")
        #obj.addProperty("App::PropertyLink", "SubsystemTo", "Subsystem", "Subsystem the coupling ends.")
        #obj.SubsystemFrom = subsystem_from
        #obj.SubsystemTo = subsystem_to

    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'SubsystemFrom':
            if obj.SubsystemFrom == None:
                self.model.subsystem_from = None
            else:
                self.model.subsystem_from = obj.SubsystemFrom.Proxy.model
                
        if prop == 'SubsystemTo':
            if obj.SubsystemTo == None:
                self.model.subsystem_to = None
            else:
                self.model.subsystem_to = obj.SubsystemTo.Proxy.model
            
            
class Excitation(BaseClass):
    """
    Abstract base class for all Excitation adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init___(self, obj, system, subsystem, **properties):
        BaseClass.__init__(self, obj, system)
            
        obj.addProperty("App::PropertyBool","IsSeaExcitation","Excitation", "True if it is a valid SEA Excitation").IsSeaCoupling=True        
        obj.setEditorMode("IsSeaExcitation", 2)

        obj.addProperty("App::PropertyLink", "Subsystem", "Excitation", "Subsystem that is excited.")  
        
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Subsystem = subsystem
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)  
        
        if prop == 'Subsystem':
            self.model.subsystem = obj.Subsystem.Proxy.model