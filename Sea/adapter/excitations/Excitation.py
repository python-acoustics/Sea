import abc
import logging
import Sea
import numpy as np
from ..base import Base
    
class Excitation(Base):
    """
    Abstract base class for all :mod:`Sea.adapter.excitations` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, subsystem):
        Base.__init__(self, obj)
        
        obj.addProperty("App::PropertyLink", "Subsystem", "Excitation", "Subsystem that is excited.")
        obj.setEditorMode("Subsystem", 1)
        obj.Subsystem = subsystem
        
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Frequency = subsystem.Frequency
        
        
        
    def onChanged(self, obj, prop):
        Base.onChanged(self, obj, prop)  
        
        if prop == 'Frequency':
            obj.Power = np.zeros(obj.Frequency.Amount).tolist()
        
        if prop == 'Power':
            self.power = np.array(obj.Power)
        
        if prop == 'Subsystem':
            self.subsystem = obj.Subsystem.Proxy
        
    def execute(self, obj):
        Base.execute(self, obj)
        
        obj.Power = obj.Proxy.power.tolist()