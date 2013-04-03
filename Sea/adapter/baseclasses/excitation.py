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
        
        obj.Model.subsystem = subsystem.Model
        
        obj.addProperty("App::PropertyFloatList", "Power", "Excitation", "Input power with which the subsystem is excited.")
        
        obj.Frequency = subsystem.Frequency
        
        
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)  
        
        if prop == 'Frequency':
            obj.Model.power = np.zeros(len(obj.Frequency))
        
        if prop == 'Power':
            obj.Model.power = np.array(obj.Power)
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        obj.Power = obj.Model.power.tolist()