import abc
import logging
import Sea
import numpy as np

from ..base import Base

class Coupling(Base):
    """
    Abstract base class for all :mod:`Sea.adapter.couplings` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, connection, subsystem_from, subsystem_to):
        Base.__init__(self, obj)
        
        obj.addProperty("App::PropertyLink", "Connection", "Coupling", "Connection this coupling is part of.")
        obj.Connection = connection
        
        obj.Frequency = connection.Frequency
        
        obj.Label = obj.ClassName + '_' + subsystem_from.ClassName.replace('Subsystem', '') + '_to_' + subsystem_to.ClassName.replace('Subsystem', '')
        
        obj.addProperty("App::PropertyFloatList", "CLF", "Coupling", "Coupling loss factor.")
        
        obj.addProperty("App::PropertyLink", "SubsystemFrom", "Coupling", "Subsystem from")
        obj.addProperty("App::PropertyLink", "SubsystemTo", "Coupling", "Subsystem to")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceFrom", "Subsystem From", "Impedance of connection corrected From subsystem.")     
        obj.addProperty("App::PropertyFloatList", "ResistanceFrom", "Subsystem From", "Resistance of connection corrected From subsystem.")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceTo", "Subsystem To", "Impedance of connection corrected To subsystem.")
        obj.addProperty("App::PropertyFloatList", "ResistanceTo", "Subsystem To", "Resistance of connection corrected To subsystem.")
        
        
        """How or more specifically, when to update the size of the coupling?"""
        #obj.addProperty("App::PropertyFloat", "Size", "Coupling", "Size of the junction.")
        
        #subsystem_from.CouplingsFrom = subsystem_from.CouplingsFrom + [obj]
        #subsystem_to.CouplingsTo = subsystem_to.CouplingsTo + [obj]
        
        obj.SubsystemFrom = subsystem_from
        obj.SubsystemTo = subsystem_to
        
    def onChanged(self, obj, prop):
        Base.onChanged(self, obj, prop)
        
        
        if prop == 'SubsystemFrom':
            obj.Proxy.subsystem_from = obj.SubsystemFrom.Proxy
        if prop == 'SubsystemTo':
            obj.Proxy.subsystem_to = obj.SubsystemTo.Proxy
            

    def execute(self, obj):
        Base.execute(self, obj)
        
        obj.CLF = obj.Proxy.clf.tolist()
        obj.ImpedanceFrom = obj.Proxy.impedance_from.tolist()
        obj.ImpedanceTo = obj.Proxy.impedance_to.tolist()
        obj.ResistanceFrom = obj.Proxy.resistance_from.tolist()
        obj.ResistanceTo = obj.Proxy.resistance_to.tolist()
    
    
    #@abc.abstractmethod
    #def size(self, obj):
        #"""
        #Return the size of the coupling.
        #"""
        #return
        