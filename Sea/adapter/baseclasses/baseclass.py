import abc
import logging
#import FreeCAD as App

#import FreeCAD, FreeCADGui
#from pivy import coin

#import Sea

import numpy as np


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
    
    def __init__(self, obj, sea_object):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        """
        #system.Objects = system.Objects + [obj]
        
        obj.touch()
        obj.Proxy = self
        
        obj.addProperty("App::PropertyString", "ClassName", "SEA", "Name of the class of this object.")
        obj.addProperty("App::PropertyString", "SeaObject", "SEA", "Type of SEA object.")
        obj.addProperty("App::PropertyFloatList", "Frequency", "SEA", "Frequency bands")
        
        obj.SeaObject = sea_object       
        obj.ClassName = self.__class__.__name__
        
        obj.Label = obj.ClassName
        
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
            self.model.frequency = np.array(obj.Frequency)
            
    def execute(self, obj):
        """
        This method will be executed on a recomputation.
        
        :param obj: Feature object
        """
        pass

    @staticmethod
    def toList(x):
        """
        Convert :attr:`x` to a list of floats.
        """
        return map(float, list(x))
    
    
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

