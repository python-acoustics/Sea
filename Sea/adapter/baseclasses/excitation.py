import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass
    
class Excitation(BaseClass):
    """
    Abstract base class for all :mod:`Sea.adapter.excitations` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init___(self, obj, system, component, subsystem, model):
        BaseClass.__init__(self, obj, model)
        system.Excitations = system.Excitations + [obj]
        
        obj.addProperty("App::PropertyLink", "Component", "Excitation", "Component that is excited.")  
        obj.addProperty("App::PropertyString", "Subsystem", "Excitation", "Subsystem that is excited.")  
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Frequency = system.Frequency
        obj.Component = component
        obj.Subsystem = subsystem
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)  
        
        if prop == 'Subsystem':
            self.model.subsystem = obj.Subsystem.Proxy.model