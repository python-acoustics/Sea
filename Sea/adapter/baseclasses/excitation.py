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
    
    def __init__(self, obj, subsystem, model):
        BaseClass.__init__(self, obj, model)
        subsystem.Excitations = subsystem.Excitations + [obj]
        
        obj.Proxy.model.subsystem = subsystem.Proxy.model
        
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Frequency = subsystem.Frequency
        
        
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)  
        
        if prop == 'Frequency':
            obj.Proxy.model.power = np.zeros(obj.Frequency.Amount)
        
        if prop == 'Power':
            obj.Proxy.model.power = np.array(obj.Power)
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        obj.Power = obj.Proxy.model.power.tolist()