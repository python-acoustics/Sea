import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Coupling(BaseClass):
    """
    Abstract base class for all :mod:`Sea.adapter.couplings` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to):
        BaseClass.__init__(self, obj, 'Coupling')
        
        #print connection.ClassName
        connection.Couplings = connection.Couplings + [obj]
        obj.Frequency = connection.Frequency
        
        
        
        
        obj.addProperty("App::PropertyFloatList", "CLF", "Coupling", "Coupling loss factor.")
        
        obj.addProperty("App::PropertyString", "ComponentFrom", "Coupling", "Component from")
        obj.addProperty("App::PropertyString", "ComponentTo", "Coupling", "Component to")
        obj.addProperty("App::PropertyString", "SubsystemFrom", "Coupling", "Subsystem from")
        obj.addProperty("App::PropertyString", "SubsystemTo", "Coupling", "Subsystem to")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceFrom", "Subsystem From", "Impedance of connection corrected From subsystem.")     
        obj.addProperty("App::PropertyFloatList", "ResistanceFrom", "Subsystem From", "Resistance of connection corrected From subsystem.")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceTo", "Subsystem To", "Impedance of connection corrected To subsystem.")
        obj.addProperty("App::PropertyFloatList", "ResistanceTo", "Subsystem To", "Resistance of connection corrected To subsystem.")
        
        
        """How or more specifically, when to update the size of the coupling?"""
        #obj.addProperty("App::PropertyFloat", "Size", "Coupling", "Size of the junction.")
        
        #component_from.CouplingsFrom = component_from.CouplingsFrom + [obj]
        #component_to.CouplingsTo = component_to.Couplingsto + [obj]
        subsystem_from.CouplingsFrom = subsystem_from.CouplingsFrom + [obj]
        subsystem_to.CouplingsTo = subsystem_to.CouplingsTo + [obj]
        
        
        obj.ComponentFrom = component_from.Name
        obj.ComponentTo = component_to.Name
        obj.SubsystemFrom = subsystem_from.Name
        obj.SubsystemTo = subsystem_to.Name
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        
        if prop == 'SubsystemFrom':
            self.model.subsystem_from = obj.Document.getObject(obj.SubsystemFrom).Proxy.model
        elif prop == 'SubsystemTo':
            self.model.subsystem_to = obj.Document.getObject(obj.SubsystemTo).Proxy.model
            

    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        obj.CLF = self.model.clf
        
        obj.ImpedanceFrom = map(float, list(self.model.impedance_from))
        obj.ImpedanceTo = map(float, list(self.model.impedance_to))
        obj.ResistanceFrom = map(float, list(self.model.resistance_from))
        obj.ResistanceTo = map(float, list(self.model.resistance_to))
    
    
    #@abc.abstractmethod
    #def size(self, obj):
        #"""
        #Return the size of the coupling.
        #"""
        #return
        