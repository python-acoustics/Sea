import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Subsystem(BaseClass):
    """
    Abstract base class for all Subsystem adapter classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component, model):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
        """
        
        self.model = model()
        self.model.component = component.Proxy.model
        
        BaseClass.__init__(self, obj, 'Subsystem')
        obj.Frequency = component.Frequency
        component.Subsystems = component.Subsystems + [obj]
        
        obj.addProperty("App::PropertyFloatList", "Impedance", "Subsystem", "Impedance")
        obj.addProperty("App::PropertyFloatList", "Resistance", "Subsystem", "Resistance")
        obj.addProperty("App::PropertyFloatList", "Mobility", "Subsystem", "Mobility")
        obj.addProperty("App::PropertyFloatList", "ModalDensity", "Subsystem", "Modal density")
        
                
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        

    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        
        #obj.Impedance = self.model.impedance
        #obj.Resistance  = self.model.resistance
        #obj.Mobility = self.model.mobility
        
        #print self.model.modal_density
        #obj.ModalDensity = map(float, list(self.model.modal_density))
        
       